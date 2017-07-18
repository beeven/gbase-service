import win32serviceutil
import win32service
import win32event
import servicemanager
import asyncio
import functools
import threading
from gbaseserver import GBaseServer


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "GBaseService"
    _svc_display_name_ = "GBase http service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)

        self.server = GBaseServer()
        #socket.setdefaulttimeout(60)

    @staticmethod
    def set_stop_event(event):
        with open(r"c:\test.txt","a") as f:
            f.write("setting event {0}\n".format(threading.current_thread().name))
        event.set()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        with open(r"c:\test.txt","a") as f:
            f.write("stopping {0}\n".format(threading.current_thread().name))

        self.server.stop_server()
        
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,'Started'))
        self.main()

    def main(self):

        with open(r"c:\test.txt","w") as f:
            f.write("started {0}\n".format(threading.current_thread().name))

        self.server.start_server()

        with open(r"c:\test.txt","a") as f:
            f.write("stopped {0}\n".format(threading.current_thread().name))
            
        pass

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
