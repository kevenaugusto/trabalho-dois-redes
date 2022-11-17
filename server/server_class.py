import socket
import tqdm
import os

from pathlib import Path
from util.delete_methods import delete

SEPARATOR = '<SEPARATOR>'
RECEIVED = '<RECEIVED>'
EOF = '<EOF>'
GET = '<GET>'
POST = '<POST>'
PUT = '<PUT>'
DELETE = '<DELETE>'

OUTPUT_PATH = Path(__file__).parent.parent / 'shared'

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
        client, address = self._connection.accept()
        print(f'Conectado com {address}')
        while (self._keep_alive):
            client_recv = client.recv(BUFFER_SIZE)
            if (not client_recv):
                print(f'Encerrando a conexão com {address}')
                break
            request_type, parameter = client_recv.decode().split(SEPARATOR)
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
                progress = tqdm.tqdm(range(int(parameter)), f'Receiving {request_type}', unit='B', unit_scale=True, unit_divisor=1024)
                with open(OUTPUT_PATH / request_type, 'wb+') as file:
                    while True:
                        bytes_read = client.recv(BUFFER_SIZE)
                        if (bytes_read.decode() == EOF):
                            break
                        file.write(bytes_read)
                        client.sendall(f'{RECEIVED}'.encode())
                        progress.update(len(bytes_read))
                client.sendall(f'O arquivo {request_type} foi recebido com sucesso!'.encode())
                progress.close()
        client.close()
