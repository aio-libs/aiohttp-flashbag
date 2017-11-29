aiohttp_flashbag
================

The library provides flashbag for `aiohttp.web`__.

.. _aiohttp_web: https://docs.aiohttp.org/en/stable/

__ aiohttp_web_

.. image:: https://img.shields.io/travis/wikibusiness/aiohttp-flashbag.svg
    :target: https://travis-ci.org/wikibusiness/aiohttp-flashbag

.. image:: https://codecov.io/github/wikibusiness/aiohttp-flashbag/coverage.svg
    :target: https://codecov.io/github/wikibusiness/aiohttp-flashbag

Usage
-----

The library allows us to share some data between requests inside session.

Basic usage example:

.. code-block:: python

    import aiohttp_flashbag
    from aiohttp import web
    from aiohttp_session import setup as setup_session
    from aiohttp_session import SimpleCookieStorage


    async def handler_get(request):
        validation_error = aiohttp_flashbag.flashbag_get(request, 'error')

        error_html = ''

        if validation_error is not None:
            error_html = '<span>{validation_error}</span>'.format(
                validation_error=validation_error,
            )

        body = '''
            <html>
                <head><title>aiohttp_flashbag demo</title></head>
                <body>
                    <form method="POST" action="/">
                        <input type="text" name="name" />
                        {error_html}
                        <input type="submit" value="Say hello">
                    </form>
                </body>
            </html>
        '''
        body = body.format(error_html=error_html)

        return web.Response(body=body.encode('utf-8'), content_type='text/html')


    async def handler_post(request):
        post = await request.post()

        if len(post['name']) == 0:
            aiohttp_flashbag.flashbag_set(request, 'error', 'Name is required')

            return web.HTTPSeeOther('/')

        body = 'Hello, {name}'.format(name=post['name'])

        return web.Response(body=body.encode('utf-8'), content_type='text/html')


    def make_app():
        session_storage = SimpleCookieStorage()

        app = web.Application()

        setup_session(app, session_storage)

        app.middlewares.append(aiohttp_flashbag.flashbag_middleware)

        app.router.add_route(
            'GET',
            '/',
            handler_get,
        )

        app.router.add_route(
            'POST',
            '/',
            handler_post,
        )

        return app


    web.run_app(make_app())




First of all, you have to register ``aiohttp_flashbag.flashbag_middleware`` in ``aiohttp.web.Application``.

You can get some data from the previous request with ``aiohttp_flashbag.flashbag_get`` method. Parameters:

- **request**. Instance of ``aiohttp.web_request.Request``.
- **key**. Name of "variable" that you want to get
- **default**. The default value that should be returned, if the key doesn't exist in session flashbag.

To set one "variable" in flashbag you should use ``aiohttp_flashbag.flashbag_set``. Parameters:

- **request**. Instance of ``aiohttp.web_request.Request``.
- **key**. Name of "variable" that you want to specify.
- **value**. Data that you want to specify.

If you need to replace all "variables" in flashbag you should use ``aiohttp_flashbag.flashbag_replace_all``. Parameters:

- **request**. Instance of ``aiohttp.web_request.Request``.
- **value**. Dict with values that you want to add into flashbag.

