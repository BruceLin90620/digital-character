import threading
import socket
import json
import time
import sys

# sys.path.append("/home/bruce/CSL_work/digital-character/driver")
sys.path.append("/home/ubuntu/digital-character/driver")
from control_cmd import ControlCmd, LED_OFF, LED_ON

class Server():
    def __init__(self, server_ip, unity_ip, port):

        # self.incoming_TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.incoming_TCP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.incoming_TCP_socket.bind((server_ip, port))
        # self.incoming_TCP_socket.listen(5)


        self.incoming_UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.incoming_UDP_socket.bind((server_ip, port))

        self.unity_ip = unity_ip

        self.unitySocketClient = UnitySocketClient(self.incoming_UDP_socket)

    def scanForClientConnection(self):
        while 1:
            # tcp_client_conn, tcp_client_addr = self.incoming_TCP_socket.accept()

            # print(tcp_client_addr[0], self.unity_ip)
            # if tcp_client_addr[0] == self.unity_ip:
                # self.unitySocketClient.scanForUnityClientConnection(tcp_client_conn, tcp_client_addr)
            self.unitySocketClient.scanForUnityClientConnection()
            time.sleep(1)

HOST = '10.100.3.18' 
PORT = 8000


class UnitySocketClient():
    def __init__(self, incoming_unity_socket):
        self.control_cmd = ControlCmd()
        self.incoming_unity_socket = incoming_unity_socket
        self.isconnected = False
        
    def handleClient(self, client_socket):
        while True:
            try:
                all_servo_position = self.control_cmd.read_motor_data()
                print(all_servo_position)
                msg = json.dumps(all_servo_position)
                # msg = "1"
                # client_socket.sendto(b"Hello!\n" , (HOST, PORT))
                client_socket.sendto(bytes(msg, encoding="utf-8"),  (HOST, PORT))
                # print("Hello!\n")
                time.sleep(0.001)
            except InterruptedError:
                print("InterruptedError")
                client_socket.close()

    def scanForUnityClientConnection(self):
        try:
            
            # print("Connect to Unity Client Success, addr: {}".format(unity_client_addr))
            # client_thread = threading.Thread(target=self.handleClient, args=(unity_client_conn, 
            #                                 unity_client_addr))
            if self.isconnected == False:
                client_thread = threading.Thread(target=self.handleClient, args=(self.incoming_unity_socket,))
                client_thread.start()
                self.isconnected = True
    
        except socket.error:
            print(socket.error)

if __name__ == "__main__":
    server_ip = '10.100.3.66'
    # unity_ip = '10.100.2.48' 
    unity_ip = '10.100.3.18'
    port = 8000

    demo_server = Server(server_ip, unity_ip, port)
    demo_server.scanForClientConnection()