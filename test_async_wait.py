import asyncio
import functools



def set_event(event):
    print("setting event in callback")
    event.set()

async def stop_jobs(loop, event):
    print("Do some jobs")
    await asyncio.sleep(5)
    print("Calling set_event")
    loop.call_soon(functools.partial(set_event, event))

async def do_long_waited_job(loop, event):
    print("Do long waited job and wait")
    await event.wait()


def main():
    print("Process begin")
    event = asyncio.Event()
    event_loop = asyncio.get_event_loop()
    asyncio.ensure_future(stop_jobs(event_loop, event),loop=event_loop)
    event_loop.run_until_complete(do_long_waited_job(event_loop,event))
    event_loop.close()


if __name__ == "__main__":
    main()

