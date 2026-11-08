import serial
import time

ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 115200
ser.timeout = 1
ser.rts = False
ser.dtr = False
ser.open()

print("Puerto abierto. Esperando datos...")
while True:
    n = ser.in_waiting
    if n > 0:
        datos = ser.read(n)
        print(f"Recibidos {len(datos)} bytes")
    time.sleep(0.1)