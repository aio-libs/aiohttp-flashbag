import json

import aiohttp_flashbag
import pytest
from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session import SimpleCookieStorage

flash_message = {
    'key': 'some_key',
    'value': [
        {
            'key11': 'val11',
            'key12': 'val12',
        },
        {
            'key21': 'val21',
            'key22': 'val22',
        },
    ],
    'default': 'default value',
}


async def handler_get_ok(request):
    message = aiohttp_flashbag.flashbag_get(
        request,
        flash_message['key'],
        flash_message['default'],
    )
    if not isinstance(message, str):
        message = json.dumps(message)

    return web.Response(body=message)


async def handler_post_ok_set_message(request):
    aiohttp_flashbag.flashbag_set(
        request,
        flash_message['key'],
        flash_message['value'],
    )
    return web.Response(body=b'ok')


async def handler_post_ok_append_list(request):
    values_list = flash_message['value']
    key = flash_message['key']

    for value in values_list:
        aiohttp_flashbag.flashbag_append(request, key, value)

    return web.Response(body=b'ok')


async def handler_post_exception_append_list(request):
    values_list = flash_message['value']
    key = flash_message['key']

    aiohttp_flashbag.flashbag_set(request, key, 'some string')

    for value in values_list:
        aiohttp_flashbag.flashbag_append(request, key, value)

    return web.Response(body=b'ok')


async def handler_post_ok_replace_messages(request):
    aiohttp_flashbag.flashbag_set(
        request,
        'some_key',
        'some_value',
    )

    aiohttp_flashbag.flashbag_replace_all(
        request,
        {
            flash_message['key']: flash_message['value'],
        },
    )
    return web.Response(body=b'ok')


async def handler_post_exception_replace_messages(request):
    aiohttp_flashbag.flashbag_replace_all(
        request,
        'some string',
    )
    return web.Response(body=b'ok')


async def handler_post_exception(request):
    aiohttp_flashbag.flashbag_set(
        request,
        flash_message['key'],
        flash_message['value'],
    )
    raise web.HTTPBadRequest


@pytest.fixture(
    params=[
        (handler_post_ok_set_message, 200),
        (handler_post_ok_replace_messages, 200),
        (handler_post_exception_replace_messages, 500),
        (handler_post_ok_append_list, 200),
        (handler_post_exception_append_list, 500),
        (handler_post_exception, 400),
    ],
)
def handler_data(request):
    return request.param


def create_app(loop, handler_get, handler_post, flashbag_middleware=True):
    session_storage = SimpleCookieStorage()

    app = web.Application(loop=loop)

    setup_session(app, session_storage)

    if flashbag_middleware:
        app.middlewares.append(aiohttp_flashbag.flashbag_middleware)

    app.router.add_route('GET', '/', handler_get)
    app.router.add_route('POST', '/', handler_post)

    return app


async def test_flashbag(test_client, handler_data):
    handler_post, status_code = handler_data
    client = await test_client(
        create_app,
        handler_get=handler_get_ok,
        handler_post=handler_post,
    )

    response = await client.post('/')

    assert response.status == status_code

    if status_code < 500:
        response = await client.get('/')

        assert response.status == 200

        assert await response.text() == json.dumps(flash_message['value'])

        response = await client.get('/')

        assert response.status == 200

        assert await response.text() == flash_message['default']


async def test_flashbag_without_middleware(test_client, handler_data):
    handler_post, _ = handler_data
    client = await test_client(
        create_app,
        handler_get=handler_get_ok,
        handler_post=handler_post,
        flashbag_middleware=False,
    )

    response = await client.post('/')

    assert response.status == 500

    response = await client.get('/')

    assert response.status == 500
