import socket
import tqdm
import os

from pathlib import Path

SEPARATOR = '<SEPARATOR>'
GET = '<GET>'
POST = '<POST>'
PUT = '<PUT>'
DELETE = '<DELETE>'

BUFFER_SIZE = 4096 # Send 4096 bytes each time step

class Server:
    def __init__(self, host: str, port: str) -> None:
        self._keep_alive = True
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.bind((host, port))
        self._connection.listen(1)

    def __del__(self) -> None:
        self._connection.close()

    def close(self) -> None:
        self._keep_alive = False

    def receive_connection(self) -> None:
        while (self._keep_alive):
            client, address = self._connection.accept()
            request_type, parameter = client.recv(BUFFER_SIZE).decode().split(SEPARATOR)
            if (request_type == GET):
                pass
            elif (request_type == POST):
                pass
            elif (request_type == PUT):
                pass
            elif (request_type == DELETE):
                pass
            client.close()
