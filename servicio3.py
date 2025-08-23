import socket
import datetime
import sys

def send_http_request(host, port, message):
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.connect((host, port))

    request = (
        f"POST / HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(message)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{message}"
    )

    http_socket.send(request.encode('utf-8'))

    http_socket.close()

def main():
    host_udp = 'localhost'
    port_udp = 50003

    host_http_s4 = 'localhost'
    port_http_s4 = 50004

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host_udp, port_udp))

    print("Servicio S3 iniciado. Esperando mensajes UDP...")

    while True:
        data, addr = udp_socket.recvfrom(1024)
        data = data.decode('utf-8')
        print(f"Recibido de S2: {data}")

        if data.count('-') == 1 and data.rsplit('-', 1)[1] == "FIN":
            print("Señal de fin recibida de S2. Propagando a S4 via HTTP.")
            send_http_request(host_http_s4, port_http_s4, data)
            break

        parts = data.rsplit('-', 3)
        if len(parts) < 4:
            print("Formato de mensaje inválido.")
            continue

        timestamp, min_len_str, current_len_str, message = parts
        min_length = int(min_len_str)
        current_length = int(current_len_str)
        new_word = input("Ingrese una nueva palabra para agregar: ").strip()
        updated_message = f"{message} {new_word}" if message else new_word
        updated_length = len(updated_message)
        new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_formatted_message = f"{new_timestamp}-{min_length}-{updated_length}-{updated_message}"
        print(f"Enviando a S4 via HTTP: {new_formatted_message}")
        send_http_request(host_http_s4, port_http_s4, new_formatted_message)

    udp_socket.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
