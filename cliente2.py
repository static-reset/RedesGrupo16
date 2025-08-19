import asyncio
import socket
import re
import os
import http.server
import datetime

TCP_HOST = '127.0.0.1'
TCP_PORT = 5000

UDP_HOST = '127.0.0.1'
UDP_PORT = 6000

def iniciar_servidorUDP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_udp:
        servidor_udp.bind((UDP_HOST, UDP_PORT))
        servidor_udp.listen()
        print(f"El servidor está probando en {UDP_HOST}:{UDP_PORT}")
