import aiohttp_jinja2
from aiohttp import web

from aiohttp_statuscheck.debugger import dump

async def handle_404(request):
    print("hi 404")
    print("request: {}".format(request))
    print("dump(request): {}".format(request))
    response = await request.json()
    # return aiohttp_jinja2.render_template('404.html', request, {})
    if response.headers['Content-Type'] == "application/json":
        return web.json_response({
            "status": 404,
            "message": "Not Found."
        }, status=404)


async def handle_500(request):
    print("hi 500")
    print("request: {}".format(request))
    print("dump(request): {}".format(request))
    response = await request.json()
    # return aiohttp_jinja2.render_template('500.html', request, {})
    # logger.error(response.body)
    # EG: https://github.com/aio-libs/aiohttp/issues/2175
    if response.headers['Content-Type'] == "application/json":
        return web.json_response({
            "status": 503,
            "message": "Service currently unavailable."
        }, status=503)


def create_error_middleware(overrides):
    print("hi overrides")

    @web.middleware
    async def error_middleware(request, handler):

        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override:
                return await override(request)

            return response

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
