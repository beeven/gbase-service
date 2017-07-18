import asyncio
from aiohttp import web

loop = asyncio.get_event_loop()

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def shutdown(request):
    pass

app = web.Application()
app.router.add_get("/", handle)
app.router.add_get("/{name}", handle)




handler = app.make_handler()
f = loop.create_server(handler,"0.0.0.0",8080)
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())
