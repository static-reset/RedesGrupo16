import socket
import datetime
import sys

def main():
    host_s1 = 'localhost'
    port_s1 = 50001
    host_s2 = 'localhost'
    port_s2 = 50002

    #SOCKETS
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_s1, port_s1))
    server_socket.listen(1)

    #DATOS INICIALES
    min_length = int(input("Ingrese el largo mínimo del mensaje: "))
    initial_word = input("Ingrese la palabra inicial: ").strip()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_length = len(initial_word)
    message = initial_word
    formatted_message = f"{timestamp}-{min_length}-{current_length}-{message}"
    client_socket_s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_s2.connect((host_s2, port_s2))
    client_socket_s2.send(formatted_message.encode('utf-8'))
    print(f"Enviado a S2: {formatted_message}")
    client_socket_s2.close()

    running = True
    while running:
        conn, addr = server_socket.accept()
        data = conn.recv(1024).decode('utf-8')
        
        if not data:
            conn.close()
            continue
        print(f"Recibido de S4: {data}")

        if data.count('-') == 1 and data.rsplit('-', 1)[1] == "FIN":
            print("Señal de fin recibida. Propagando a S2 y cerrando.")
            client_socket_s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket_s2.connect((host_s2, port_s2))
            client_socket_s2.send(data.encode('utf-8'))
            client_socket_s2.close()
            conn.close()
            running = False 
            continue

        parts = data.rsplit('-', 3)
        if len(parts) < 4:
            print(f"Formato de mensaje inválido: {data}")
            conn.close()
            continue

        timestamp, min_len_str, current_len_str, message = parts
        
        try:
            min_length = int(min_len_str)
            current_length = int(current_len_str)
        except ValueError:
            print(f"Error en formato numérico del mensaje: {data}")
            conn.close()
            continue

        new_word = input("Ingrese una nueva palabra para agregar: ").strip()
        updated_message = f"{message} {new_word}" if message else new_word
        updated_length = len(updated_message)
        new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_formatted_message = f"{new_timestamp}-{min_length}-{updated_length}-{updated_message}"
        client_socket_s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket_s2.connect((host_s2, port_s2))
        client_socket_s2.send(new_formatted_message.encode('utf-8'))
        print(f"Enviado a S2: {new_formatted_message}")
        client_socket_s2.close()
        conn.close()

    server_socket.close()
    print("Servicio S1 finalizado.")
    sys.exit(0)

if __name__ == "__main__":
    main()