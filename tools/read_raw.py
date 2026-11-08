import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
print("Abierto. Esperando...")
while True:
    n = ser.in_waiting
    if n > 0:
        datos = ser.read(n)
        print(f"Recibidos {len(datos)} bytes: {datos[:20].hex()}")
    time.sleep(0.1)
    