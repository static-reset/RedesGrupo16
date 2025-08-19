import asyncio
import socket
import re
import os
import http.server
from datetime import datetime

tamanio_min = input("Hola, por favor indica que tan largo quieres que sea el mensaje: ")
mensaje_tcp = input("Ahora ingresa la palabra para iniciar el mensaje: ")

TCP_HOST = '127.0.0.1'
TCP_PORT = 5000

def iniciar_servidorTCP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_tcp:
        servidor_tcp.bind((TCP_HOST, TCP_PORT))
        servidor_tcp.listen()
        print(f"El servidor está probando en {TCP_HOST}:{TCP_PORT}")

def formatear(mensaje):
    timestamp = datetime.now()
    largo_actual = len(mensaje)
    return f"{timestamp}-{tamanio_min}-{largo_actual}-{mensaje}"


iniciar_servidorTCP()
print(formatear(mensaje_tcp))