import asyncio
import functools
from aiohttp import web

class GBaseServer(object):
    def __init__(self, loop=None):
        self.event_loop = loop if loop is not None else asyncio.get_event_loop()
        self.app = web.Application()
        self.init_app()
        self.wait_event = asyncio.Event(loop=self.event_loop)
        
    def start_server(self):
        handler = self.app.make_handler(loop=self.event_loop)
        future = self.event_loop.create_server(handler,"0.0.0.0",8080)
        srv = self.event_loop.run_until_complete(future)
        print("serving on", srv.sockets[0].getsockname())
        self.event_loop.run_until_complete(self.long_waited_job())
        print("cleaning up")
        srv.close()
        self.event_loop.run_until_complete(srv.wait_closed())
        self.event_loop.run_until_complete(self.app.shutdown())
        self.event_loop.run_until_complete(handler.shutdown(60.0))
        self.event_loop.run_until_complete(self.app.cleanup())
        print("cleaned up")

        self.event_loop.close()


    def stop_server(self):
        self.event_loop.call_soon_threadsafe(functools.partial(GBaseServer.set_stop_event, self.wait_event))
    
    @staticmethod
    def set_stop_event(event):
        event.set()

    async def long_waited_job(self):
        await self.wait_event.wait()
    
    def init_app(self):
        self.app.router.add_get("/", self.intro_handler)
        self.app.router.add_get("/{entry_id}",self.entry_detail_handler)

        async def on_shutdown(app):
            print("shutting down app...")
            await asyncio.sleep(2)
            print("shutted down app")

        self.app.on_shutdown.append(on_shutdown)


    async def entry_detail_handler(self, request):
        entry_id = request.match_info.get('entry_id',"No ID")
        text = "The details of entry {0} is as follow".format(entry_id)
        return web.Response(text=text)

    async def intro_handler(self, request):
        return web.Response(text="Hello")
    





if __name__=="__main__":

    import threading,time

    def worker(server):
        server.start_server()
    
    def signal(server):
        print("shutting down in 3 seconds")
        time.sleep(3)
        print("calling server.stop_server")
        server.stop_server()
    

    server = GBaseServer()

    w = threading.Thread(target=worker, args=(server,))
    w.start()

    s = threading.Thread(target=signal, args=(server,))
    s.start()

    w.join()

    
    #server.start_server()