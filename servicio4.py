import socket
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import sys

HOST_S1 = 'localhost'
PORT_S1 = 50001

class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(f"Recibido HTTP: {post_data}")

        if post_data.count('-') == 1 and post_data.rsplit('-', 1)[1] == "FIN":
            print("Señal de fin recibida de S3. Iniciando secuencia de fin.")
            self.send_response(200)
            self.end_headers()
            self.wfile.write("FIN recibido".encode('utf-8'))
            initiate_shutdown_sequence(post_data)
            return

        parts = post_data.rsplit('-', 3)
        if len(parts) < 4:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Formato inválido".encode('utf-8'))
            return

        timestamp, min_len_str, current_len_str, message = parts
        min_length = int(min_len_str)
        current_length = int(current_len_str)

        if current_length >= min_length:
            # Mensaje completo - guardar y enviar FIN
            save_message_to_file(timestamp, min_length, current_length, message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Mensaje guardado, iniciando fin".encode('utf-8'))
            fin = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-FIN"
            initiate_shutdown_sequence(fin)
        else:
            new_word = input("Ingrese una nueva palabra para agregar: ").strip()
            updated_message = f"{message} {new_word}" if message else new_word
            updated_length = len(updated_message)
            new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_formatted_message = f"{new_timestamp}-{min_length}-{updated_length}-{updated_message}"
            send_to_s1(new_formatted_message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Mensaje enviado a S1 para continuar".encode('utf-8'))

def send_to_s1(message):
    try:
        s1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1_socket.connect((HOST_S1, PORT_S1))
        s1_socket.send(message.encode('utf-8'))
        print(f"Enviado a S1: {message}")
        s1_socket.close()
    except Exception as e:
        print(f"Error enviando a S1: {e}")

def save_message_to_file(timestamp, min_length, current_length, message):
    filename = f"mensaje_final_{timestamp.replace(' ', '_').replace(':', '-')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{timestamp}-{min_length}-{current_length}-{message}")
    print(f"Mensaje guardado en {filename}")

def initiate_shutdown_sequence(fin_message):
    print("Iniciando secuencia de finalización...")
    send_to_s1(fin_message)
    threading.Timer(1.0, graceful_shutdown).start()

def graceful_shutdown():
    print("Cerrando servidor S4...")
    http_server.shutdown()

def run_http_server():
    global http_server
    server_address = ('localhost', 50004)
    http_server = HTTPServer(server_address, HTTPHandler)
    print("Servidor HTTP S4 iniciado en puerto 50004...")
    http_server.serve_forever()

def main():
    server_thread = threading.Thread(target=run_http_server)
    server_thread.daemon = True
    server_thread.start()

    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("\nCerrando S4...")
        graceful_shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()