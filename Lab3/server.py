from PIL import Image
import socket
from sobel import div_img, join_img
from client import send_all, receive_all


def server_main(image_path, n_clients):
    image = Image.open(image_path)
    fragments = div_img(image, n_clients)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 2040))
    server_socket.listen(n_clients)

    print("Serwer nasluchuje...")

    processed_fragments = []

    for i in range(n_clients):
        client_socket, client_address = server_socket.accept()
        print(f"Polaczono z klientem {i + 1}: {client_address}")

        send_all(client_socket, fragments[i])
        processed_fragment = receive_all(client_socket)
        processed_fragments.append(processed_fragment)
        client_socket.close()

    result_image = join_img(processed_fragments)
    result_image.save("processed_image.png")

    print("Obraz przetworzony zapisany jako processed_image.png")


if __name__ == '__main__':
    server_main('img1.png', 3)