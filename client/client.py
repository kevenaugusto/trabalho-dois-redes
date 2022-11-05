import socket
import tqdm
import os

SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 4096 # Send 4096 bytes each time step

class Client:
    def __init__(self, host: str, port: str) -> None:
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect((host, port))

    def __del__(self) -> None:
        self._connection.close()

    def update_directories(self):
        pass

    def upload_file(self, filename: str) -> None:
        filesize = os.path.getsize(filename)
        # Send the filename and filesize
        self._connection.send(f'{filename}{SEPARATOR}{filesize}'.encode())
        # Start sending the file
        progress = tqdm.tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)
        with open(filename, 'rb') as file:
            while (True):
                # Read the bytes from the file
                bytes_read = file.read(BUFFER_SIZE)
                if (not bytes_read):
                    # File transmitting is done
                    break
                # We use sendall to assure transmission in busy networks
                self._connection.sendall(bytes_read)
                # Update the progress bar
                progress.update(len(bytes_read))

    def delete_file(self):
        pass
        
    def create_directory(self):
        pass

    def delete_directory(self):
        pass


