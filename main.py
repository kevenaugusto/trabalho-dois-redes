from server.server_class import Server
from client.client_class import Client
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
OUTPUT_PATH = OUTPUT_PATH / 'shared'

def main():
    host = input('Host: ')
    port = int(input('Port: '))
    option = input('Digite [1] para Servidor e [2] para Cliente: ')
    match option:
        case '1':
            server = Server(host, port)
            print('\nPressione Ctrl+C para encerrar a execução...\n')
            server.receive_connection()
        case '2':
            client = Client(host, port)
            keep_loop = True
            print() # Line Break
            while (keep_loop):
                print('[1] Atualizar Diretório')
                print('[2] Carregar Arquivo')
                print('[3] Remover Arquivo/Diretório')
                print('[4] Criar Diretório')
                print('[5] Encerrar\n')
                option = input('O que deseja realizar?: ')
                match option:
                    case '1':
                        print(f'\n{client.update_directories(OUTPUT_PATH)}\n')
                    case '2':
                        filepath = input('Caminho do Arquivo: ')
                        print(f'\n{client.upload_file(filepath)}\n')
                    case '3':
                        path = input('Caminho do Arquivo/Diretório: ')
                        print(f'\n{client.delete(OUTPUT_PATH / path)}\n')
                    case '4':
                        name = input('Nome do Diretório: ')
                        print(f'\n{client.create_directory(OUTPUT_PATH / name)}\n')
                    case '5':
                        print('Encerrando...')
                        del(client) # Closes server connection
                        keep_loop = False
                    case _:
                        print('Opção inválida.../n')
        case _:
            print('Opção não definida...')

if __name__ == '__main__':
    main()