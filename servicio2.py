import socket
import datetime
import sys

def main():
    host_tcp = 'localhost'
    port_tcp = 50002

    host_udp_s3 = 'localhost'
    port_udp_s3 = 50003

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((host_tcp, port_tcp))
    tcp_socket.listen(1)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Servicio S2 iniciado. Esperando conexiones...")

    while True:
        conn, addr = tcp_socket.accept()
        data = conn.recv(1024).decode('utf-8')
        if not data:
            conn.close()
            continue
        print(f"Recibido de S1: {data}")

        if data.count('-') == 1 and data.rsplit('-', 1)[1] == "FIN":
            print("Señal de fin recibida de S1. Propagando a S3.")
            udp_socket.sendto(data.encode('utf-8'), (host_udp_s3, port_udp_s3))
            conn.close()
            break

        parts = data.rsplit('-', 3)
        if len(parts) < 4:
            print("Formato de mensaje inválido.")
            conn.close()
            continue

        timestamp, min_len_str, current_len_str, message = parts
        min_length = int(min_len_str)
        current_length = int(current_len_str)
        new_word = input("Ingrese una nueva palabra para agregar: ").strip()
        updated_message = f"{message} {new_word}" if message else new_word
        updated_length = len(updated_message)
        new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_formatted_message = f"{new_timestamp}-{min_length}-{updated_length}-{updated_message}"
        udp_socket.sendto(new_formatted_message.encode('utf-8'), (host_udp_s3, port_udp_s3))
        print(f"Enviado a S3: {new_formatted_message}")
        conn.close()

    udp_socket.close()
    tcp_socket.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
