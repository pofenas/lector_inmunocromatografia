import serial
import sys
import time
import os

PUERTO = '/dev/ttyUSB0'
BAUDIOS = 115200

START = bytes([0xAA, 0x55])
END = bytes([0x55, 0xAA])

CARPETA = 'img'


def main():
    os.makedirs(CARPETA, exist_ok=True)

    ser = serial.Serial()
    ser.port = PUERTO
    ser.baudrate = BAUDIOS
    ser.timeout = 1
    ser.rts = False
    ser.dtr = False
    ser.open()
    print(f"Escuchando en {PUERTO}...")
    print(f"Guardando en ./{CARPETA}/")

    buffer = bytearray()
    contador = 0

    while True:
        n = ser.in_waiting
        if n > 0:
            datos = ser.read(n)
            buffer.extend(datos)

            inicio = buffer.find(START)
            if inicio == -1:
                if len(buffer) > 2:
                    buffer = buffer[-2:]
                continue

            fin = buffer.find(END, inicio + len(START))
            if fin == -1:
                continue

            imagen = buffer[inicio + len(START):fin]
            nombre = os.path.join(CARPETA, f"captura{contador}.jpg")
            with open(nombre, "wb") as f:
                f.write(imagen)
            print(f"Guardada {nombre} ({len(imagen)} bytes)")

            contador += 1
            buffer = buffer[fin + len(END):]
        else:
            time.sleep(0.05)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDetenido.")
        sys.exit(0)