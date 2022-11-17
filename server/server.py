import socket
import tqdm
import os

from pathlib import Path
from util.delete_methods import delete

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
                data = '' # Needs to execute data.pop(0) after decode().split(SEPARATOR)
                for directory in os.listdir(parameter):
                    data = data + SEPARATOR + directory
                client.sendall(data.encode())
            elif (request_type == POST):
                Path(parameter).mkdir(parents=True, exist_ok=True)
                client.sendall(f'A pasta {parameter} foi criada com sucesso!'.encode())
            elif (request_type == PUT):
                raise Exception('Not implemented yet')
            elif (request_type == DELETE):
                try:
                    delete(Path(parameter))
                    client.sendall(f'O diretório/arquivo {parameter} foi removido com sucesso!'.encode())
                except Exception as error:
                    print(error)
            else:
                # HERE REQUEST_TYPE IS THE FILE NAME                
                filesize = int(parameter)
                # start receiving the file from the socket
                # and writing to the file stream
                progress = tqdm.tqdm(range(filesize), f'Receiving {request_type}', unit='B', unit_scale=True, unit_divisor=1024)
                with open(request_type, 'wb') as f:
                    while True:
                        # read 1024 bytes from the socket (receive)
                        bytes_read = client.recv(BUFFER_SIZE)
                        if not bytes_read:
                            # nothing is received
                            # file transmitting is done
                            break
                        # write to the file the bytes we just received
                        f.write(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read))
                client.sendall(f'O arquivo {request_type} foi recebido com sucesso!'.encode())
            client.close()
