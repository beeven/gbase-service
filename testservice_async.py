import win32serviceutil
import win32service
import win32event
import servicemanager
import asyncio
import functools
import threading


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "TestServiceAsync"
    _svc_display_name_ = "Test Service with Asyncio"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        #self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.event_loop = asyncio.get_event_loop()
        self.wait_event = asyncio.Event(loop=self.event_loop)
        #socket.setdefaulttimeout(60)

    @staticmethod
    def set_stop_event(event):
        with open(r"c:\test.txt","a") as f:
            f.write("setting event {0}\n".format(threading.current_thread().name))
        event.set()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        #win32event.SetEvent(self.hWaitStop)
        with open(r"c:\test.txt","a") as f:
            f.write("stopping {0}\n".format(threading.current_thread().name))

        self.event_loop.call_soon_threadsafe(functools.partial(AppServerSvc.set_stop_event, self.wait_event))

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    async def long_waited_job(self):
        with open(r"c:\test.txt","a") as f:
            f.write("Doing job and waiting {0}\n".format(threading.current_thread().name))
        await self.wait_event.wait()

    def main(self):

        with open(r"c:\test.txt","w") as f:
            f.write("started {0}\n".format(threading.current_thread().name))
        #win32event.WaitForSingleObject(self.hWaitStop,win32event.INFINITE)
        self.event_loop.run_until_complete(self.long_waited_job())
        self.event_loop.close()


        with open(r"c:\test.txt","a") as f:
            f.write("stopped {0}\n".format(threading.current_thread().name))
            
        pass

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
