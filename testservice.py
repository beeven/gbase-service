import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import threading


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "TestService"
    _svc_display_name_ = "Test Service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        with open(r"c:\test.txt","a") as f:
            f.write("stopping {0}\n".format(threading.current_thread().name))
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        with open(r"c:\test.txt","w") as f:
            f.write("started {0}\n".format(threading.current_thread().name))
        win32event.WaitForSingleObject(self.hWaitStop,win32event.INFINITE)
        with open(r"c:\test.txt","a") as f:
            f.write("stopped {0}\n".format(threading.current_thread().name))
            
        pass

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
