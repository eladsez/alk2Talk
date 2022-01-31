import socket
from typing import List

from Utilities import packets_over_tcp

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'


class Client:

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_name = None
        except socket.error as err:
            print("ERROR, failed to create Client socket")
            raise err

    def connect(self, addr: tuple, client_name: str):
        if self.client_name is not None:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_name = None
            except socket.error as err:
                print("ERROR, failed to create Client socket")
                raise err
        self.client_name = client_name
        try:
            self.sock.connect(addr)
            self.sock.send(client_name.encode())
        except socket.error as err:
            print("ERROR, Client failed to connect the Server")
            raise err

    def disconnect(self):
        """
        This method disconnects the Client from the Server
        :return:
        """
        self.sock.send('|-exit-|'.encode())
        self.sock.close()

    def receive(self):
        try:
            pkt = self.sock.recv(1024).decode()
            print(pkt)
            screen_view = self.handle_pkt(pkt)
            if pkt == '|-bye-|':
                return
            return screen_view
        except socket.error:
            print('ERROR Client failed in receive')

    def handle_pkt(self, pkt: str):
        layers = pkt.split('|')
        if layers[0] == MSG_TYPE:
            return '\n' + layers[1] + ': ' + layers[3]

    def send_msg(self, msg, receiver_name='broadcast'):
        """
        This method sends the pkt message
        :param msg:
        :param receiver_name:
        :return:
        """
        msg = packets_over_tcp.msg_packet(self.client_name, receiver_name, msg)
        try:
            self.sock.send(msg.encode())
        except socket.error:
            print('ERROR Client failed trying to send')

    def recv_names(self, cli_names: List[str]):
        """
        This method returns all the Client names in the chat
        :return:
        """
        pass

    def recv_files(self) -> list:
        """
        This method returns all the file names in the Server.
        :return:
        """
        pass

    def request_download(self, file_name: str) -> bool:
        """
        This method checks if the request is viable to download
        :param file_name: a name of file.
        :return:
        """
        pass

    def download(self) -> object:
        """
        A simple download file method
        :return:
        """
        pass


if __name__ == '__main__':
    client = Client()
    client.connect(('127.0.0.1', 12345))
