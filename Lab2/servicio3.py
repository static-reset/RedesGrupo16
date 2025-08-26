import socket
import datetime
import sys
import json

def send_http_request(host, port, message):
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.connect((host, port))

    request = (
        f"POST /frase/ HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(message)+1}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{message}"
    )

    http_socket.send(request.encode('utf-8'))

    response = b""
    while True:
        chunk = http_socket.recv(1024)
        if not chunk:
            break
        response += chunk
    print(f"Respuesta HTTP de S4: {response.decode('utf-8', errors='ignore')}")

    http_socket.close()

def main():



    client = '192.168.1.179'
    tcp_port = 9000
    udp_port = 9001
    http_port = 1080

    str = input("Por favor indica el comando: ")
    comando = f"{str}"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((client, tcp_port))
    client_socket.send(comando.encode('utf-8'))
    print("Enviado el mensaje al servidor.")

    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        client_socket.close()
    print(f"Recibido de S: {data}")
    client_socket.close()

    mensaje_for = f"{data}"
    print(mensaje_for)
    client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket2.connect((client, udp_port))
    client_socket2.send(mensaje_for.encode('utf-8'))
    print("Enviado el mensaje al servidor.")

    data2 = client_socket2.recv(1024).decode('utf-8')
    if not data2:
        client_socket2.close()
    print(f"Mensaje recibido de S: {data2}")

    client_socket2.close()

    m = "Naty16"
    mensaje3 = f"{data2} {m}"
    print(mensaje3)
    send_http_request(client, http_port, mensaje3)
    print("Enviado el mensaje al servidor.")
        



if __name__ == "__main__":
    main()