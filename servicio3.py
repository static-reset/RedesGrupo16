import socket
import datetime
import sys

def send_http_request(host, port, message):
    """Envía una solicitud HTTP POST al servidor S4 con el mensaje en el cuerpo"""
    # Crear socket TCP para HTTP
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.connect((host, port))
    
    # Construir solicitud HTTP POST
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
    
    # Recibir respuesta (opcional, para debugging)
    response = http_socket.recv(1024).decode('utf-8')
    print(f"Respuesta HTTP de S4: {response}")
    
    http_socket.close()

def main():
    # Configuración del servidor UDP (recibe desde S2)
    host_udp = 'localhost'
    port_udp = 50003  # Mismo puerto al que S2 envía UDP

    # Configuración del cliente HTTP (envía a S4)
    host_http_s4 = 'localhost'
    port_http_s4 = 50004  # Puerto donde S4 recibe HTTP

    # Crear socket UDP para servidor
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host_udp, port_udp))

    print("Servicio S3 iniciado. Esperando mensajes UDP...")

    while True:
        # Recibir mensaje de S2 via UDP
        data, addr = udp_socket.recvfrom(1024)
        data = data.decode('utf-8')
        
        print(f"Recibido de S2: {data}")

        # Verificar si es señal de fin
        if data == "FIN":
            print("Señal de fin recibida de S2. Propagando a S4 via HTTP.")
            # Enviar fin a S4 via HTTP
            send_http_request(host_http_s4, port_http_s4, "FIN")
            break

        # Extraer partes del mensaje
        parts = data.rsplit('-', 3)
        if len(parts) < 4:
            print("Formato de mensaje inválido.")
            continue

        timestamp, min_len_str, current_len_str, message = parts
        min_length = int(min_len_str)
        current_length = int(current_len_str)

        # Solicitar nueva palabra al usuario
        new_word = input("Ingrese una nueva palabra para agregar: ").strip()

        # Concatenar sin espacios extra
        if message:
            updated_message = f"{message}{new_word}"
        else:
            updated_message = new_word

        updated_length = len(updated_message)

        new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_formatted_message = f"{new_timestamp}-{min_length}-{updated_length}-{updated_message}"
        
        # Enviar a S4 via HTTP
        print(f"Enviando a S4 via HTTP: {new_formatted_message}")
        send_http_request(host_http_s4, port_http_s4, new_formatted_message)

    # Cerrar socket
    udp_socket.close()
    sys.exit(0)

if __name__ == "__main__":
    main()