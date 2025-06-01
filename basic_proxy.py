import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    # Свързване със сървъра
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((remote_host, remote_port))

    def forward(source, destination, name):
        while True:
            try:
                data = source.recv(4096)
                if not data:
                    break

                # 👉 Модифицирай тук ако искаш (request/response)
                if name == "request":
                    print(f"[REQUEST] {data.decode(errors='ignore')}")
                    # data = data.replace(b"GET", b"POST")  # пример
                elif name == "response":
                    print(f"[RESPONSE] {data.decode(errors='ignore')}")
                    # data += b"\n<!-- Прокси Вмъкнато -->"  # пример

                destination.send(data)
            except:
                break

        source.close()
        destination.close()

    # Две нишки — една за заявка, една за отговор
    threading.Thread(target=forward, args=(client_socket, server_socket, "request")).start()
    threading.Thread(target=forward, args=(server_socket, client_socket, "response")).start()

def start_proxy(local_host, local_port, remote_host, remote_port):
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind((local_host, local_port))
    proxy.listen(5)
    print(f"[+] Proxy listening on {local_host}:{local_port}")

    while True:
        client_socket, addr = proxy.accept()
        print(f"[>] Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port)).start()

# Стартирай проксито: локално 9999, пренасочва към 8080 (локален уебсайт)
start_proxy("127.0.0.1", 8888, "127.0.0.1", 8080)

