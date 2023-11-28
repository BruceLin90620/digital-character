import threading
import socket
import json
from driver.control_cmd import ControlCmd

class Server():
    def __init__(self, server_ip, unity_ip, port):

        self.incoming_TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.incoming_TCP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.incoming_TCP_socket.bind((server_ip, port))
        self.incoming_TCP_socket.listen(5)

        self.unity_ip = unity_ip

        self.unitySocketClient = UnitySocketClient()

    def scanForClientConnection(self):
        while 1:
            tcp_client_conn, tcp_client_addr = self.incoming_TCP_socket.accept()
            print(tcp_client_addr[0], self.unity_ip)
            if tcp_client_addr[0] == self.unity_ip:
                self.unitySocketClient.scanForUnityClientConnection(tcp_client_conn, tcp_client_addr)

class UnitySocketClient():
    def __init__(self):
        self.control_cmd = ControlCmd()
    
    def handleClient(self, client_socket, addr):
        while True:
            try:
                all_servo_position = self.control_cmd.read_motor_data()
                msg = json.dumps(all_servo_position)
                
                client_socket.send(bytes(msg, encoding="utf-8"))
            except InterruptedError:
                print("InterruptedError")
                client_socket.close()

    def scanForUnityClientConnection(self, unity_client_conn, unity_client_addr):
        try:
            print("Connect to Unity Client Success, addr: {}".format(unity_client_addr))
            client_thread = threading.Thread(target=self.handleClient, args=(unity_client_conn, 
                                            unity_client_addr))
            client_thread.start()
    
        except socket.error:
            print(socket.error)

if __name__ == "__main__":
    server_ip = '10.100.3.18'
    unity_ip = '10.100.3.18' 
    port = 8000

    demo_server = Server(server_ip, unity_ip, port)
    demo_server.scanForClientConnection()