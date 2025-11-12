import pickle
import socket
from sobel import sobel_filter

def send_all(sock, data):
    data = pickle.dumps(data)
    sock.sendall(len(data).to_bytes(4, byteorder='big'))
    sock.sendall(data)

    print('INFO: fragment sent')


def receive_all(sock):
    length = int.from_bytes(sock.recv(4), byteorder='big')
    data = b''

    while len(data) < length:
        packet = sock.recv(4096)
        if not packet:
            break
        data += packet

    print('INFO: fragment received')
    return pickle.loads(data)


def client_main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 2040))

    fragment = receive_all(client_socket)
    processed_fragment = sobel_filter(fragment)

    send_all(client_socket, processed_fragment)

    client_socket.close()

    print("Fragment przetworzony i wyslany z powrotem do serwera")


if __name__ == '__main__':
    client_main()