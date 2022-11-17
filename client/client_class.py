import socket
import tqdm
import os

SEPARATOR = '<SEPARATOR>'
RECEIVED = '<RECEIVED>'
EOF = '<EOF>'
GET = '<GET>'
POST = '<POST>'
PUT = '<PUT>'
DELETE = '<DELETE>'

BUFFER_SIZE = 4096 # Send 4096 bytes each time step

class Client:
    def __init__(self, host: str, port: str) -> None:
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect((host, port))

    def __del__(self) -> None:
        self._connection.close()

    def update_directories(self, path) -> str:
        self._connection.sendall(f'{GET}{SEPARATOR}{path}'.encode())
        directories = self._connection.recv(BUFFER_SIZE).decode().split(SEPARATOR)
        directories.pop(0)
        directories = ', '.join(directories)
        return directories

    def upload_file(self, filename: str) -> str:
        filesize = os.path.getsize(filename)
        self._connection.sendall(f'{filename}{SEPARATOR}{filesize}'.encode())
        progress = tqdm.tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)
        with open(filename, 'rb') as file:
            while (True):
                bytes_read = file.read(BUFFER_SIZE)
                if (not bytes_read):
                    self._connection.sendall(f'{EOF}'.encode())
                    break
                self._connection.sendall(bytes_read)
                received = self._connection.recv(BUFFER_SIZE)
                if (received.decode() != RECEIVED):
                    raise Exception('O servidor não recebeu o arquivo!')
                progress.update(len(bytes_read))
        progress.close()
        return self._connection.recv(BUFFER_SIZE).decode()

    def delete(self, filename: str) -> str:
        self._connection.sendall(f'{DELETE}{SEPARATOR}{filename}'.encode())
        return self._connection.recv(BUFFER_SIZE).decode()
        
    def create_directory(self, folder: str) -> str:
        self._connection.sendall(f'{POST}{SEPARATOR}{folder}'.encode())
        return self._connection.recv(BUFFER_SIZE).decode()
