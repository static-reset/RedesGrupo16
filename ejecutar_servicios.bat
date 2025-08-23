@echo off
echo Iniciando Servicios...

start cmd /k "python C:\Users\natalie\OneDrive\Escritorio\Redes\servicio4.py" #EJEMPLO DE COMO IRIA
timeout /t 1

start cmd /k "python C:\Users\..\servicio3.py"
timeout /t 1

start cmd /k "python C:\Users\..\servicio3.py"
timeout /t 1

start cmd /k "python C:\Users\..\servicio3.py"

echo Todos los servicios han sido iniciados.
