@echo off
echo Iniciando Servicios...

start cmd /k "python C:\Users\natal\OneDrive\Escritorio\Redes\servicio4.py"
timeout /t 1

start cmd /k "python C:\Users\natal\OneDrive\Escritorio\Redes\servicio3.py"
timeout /t 1

start cmd /k "python C:\Users\natal\OneDrive\Escritorio\Redes\servicio2.py"
timeout /t 1

start cmd /k "python C:\Users\natal\OneDrive\Escritorio\Redes\servicio1.py"

echo Todos los servicios han sido iniciados.
