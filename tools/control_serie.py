import serial
import time
import sys
import os

PUERTO = '/dev/ttyUSB0'
BAUDIOS = 115200

START = bytes([0xAA, 0x55])
END = bytes([0x55, 0xAA])

def capturar_imagen(ser, nombre_archivo):
    print("Enviando comando de captura al ESP32...")
    
    # Limpiar cualquier byte residual que pueda haber en el buffer
    ser.reset_input_buffer() 
    
    # Enviar el comando 0x01
    ser.write(b'\x01')
    
    buffer = bytearray()
    timeout = time.time() + 10 # 10 segundos máximo de espera
    
    while time.time() < timeout:
        n = ser.in_waiting
        if n > 0:
            datos = ser.read(n)
            buffer.extend(datos)
            
            inicio = buffer.find(START)
            if inicio != -1:
                fin = buffer.find(END, inicio + len(START))
                if fin != -1:
                    imagen = buffer[inicio + len(START):fin]
                    
                    with open(nombre_archivo, "wb") as f:
                        f.write(imagen)
                    
                    print(f"Éxito: Guardada {nombre_archivo} ({len(imagen)} bytes)")
                    return True
        else:
            time.sleep(0.05)
            
    print("Error: Timeout esperando la imagen del ESP32.")
    return False

def main():
    os.makedirs('img', exist_ok=True)
    
    ser = serial.Serial()
    ser.port = PUERTO
    ser.baudrate = BAUDIOS
    ser.timeout = 1
    ser.rts = False
    ser.dtr = False
    ser.open()

    print(f"Conectado a {PUERTO}.")
    # Hacer una pausa para que el ESP32 se reinicie al abrir el puerto y muestre "Listo"
    time.sleep(2) 
    ser.reset_input_buffer() # Limpiar los mensajes de arranque

    contador = 0
    try:
        while True:
            input("\nPulsa ENTER para tomar una foto (o Ctrl+C para salir)...")
            
            nombre = f"img/captura{contador}.jpg"
            if capturar_imagen(ser, nombre):
                contador += 1
                
    except KeyboardInterrupt:
        print("\nSaliendo...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()