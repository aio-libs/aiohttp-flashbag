from aiohttp import web
from aiohttp_session import get_session

__version__ = '0.0.1'


OLD_REQUEST_KEY = 'aiohttp_flashbag_old'
NEW_REQUEST_KEY = 'aiohttp_flashbag_new'
SESSION_KEY = 'aiohttp_flashbag'


def flashbag_append(request, key, value):
    if NEW_REQUEST_KEY not in request:
        raise RuntimeError(
            'Install Flashbag middleware in your application',
        )

    old_value = request[NEW_REQUEST_KEY].get(key, [])

    if not isinstance(old_value, list):
        raise ValueError('Appending values allowed only for the lists')

    old_value.append(value)

    request[NEW_REQUEST_KEY][key] = old_value


def flashbag_set(request, key, value):
    if NEW_REQUEST_KEY not in request:
        raise RuntimeError(
            'Install Flashbag middleware in your application',
        )

    request[NEW_REQUEST_KEY][key] = value


def flashbag_replace_all(request, value):
    if NEW_REQUEST_KEY not in request:
        raise RuntimeError(
            'Install Flashbag middleware in your application',
        )

    if not isinstance(value, dict):
        raise ValueError('Value should be instance of dict')

    request[NEW_REQUEST_KEY] = value


def flashbag_get(request, key, default=None):
    if OLD_REQUEST_KEY not in request:
        raise RuntimeError(
            'Install Flashbag middleware in your application',
        )

    return request[OLD_REQUEST_KEY].get(key, default)


@web.middleware
async def flashbag_middleware(request, handler):
    session = await get_session(request)

    request[OLD_REQUEST_KEY] = session.pop(SESSION_KEY, {})
    request[NEW_REQUEST_KEY] = {}

    try:
        return await handler(request)
    finally:
        session[SESSION_KEY] = request[NEW_REQUEST_KEY]
