import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

def analizar_imagen(ruta_imagen):
    # 1. Cargar la imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: No se pudo cargar la imagen.")
        return

    # 2. Definir la Región de Interés (ROI)
    # Como la cámara está fija, sabemos más o menos dónde está la ventana.
    # Ajusta estos valores según tu imagen real (y1:y2, x1:x2)
    # Para tu dibujo, la ventana está en el centro. 
    # Vamos a recortar una franja horizontal en el centro.
    alto, ancho = img.shape
    y1, y2 = int(alto * 0.3), int(alto * 0.7) # Franja vertical central
    x1, x2 = int(ancho * 0.3), int(ancho * 0.7) # Franja horizontal central
    
    roi = img[y1:y2, x1:x2]

    # 3. Calcular el perfil de intensidad
    # Promediamos los píxeles de cada fila (eje 1 es horizontal)
    # Esto nos da un array de 1 dimensión con el brillo medio de cada fila
    perfil = np.mean(roi, axis=1)
    
    # 4. Suavizar un poco el perfil para eliminar ruido del rotulador o del papel
    # Usamos un filtro de media móvil simple
    ventana_suavizado = 5
    perfil_suave = np.convolve(perfil, np.ones(ventana_suavizado)/ventana_suavizado, mode='same')

    # 5. Graficar los resultados
    plt.figure(figsize=(10, 6))
    
    # Mostrar la imagen original con la ROI marcada
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.axhline(y=y1, color='r', linestyle='--')
    plt.axhline(y=y2, color='r', linestyle='--')
    plt.axvline(x=x1, color='r', linestyle='--')
    plt.axvline(x=x2, color='r', linestyle='--')
    plt.title("Imagen original y ROI")
    
    # Mostrar el perfil de intensidad
    plt.subplot(1, 2, 2)
    plt.plot(perfil_suave, range(len(perfil_suave)), color='blue')
    plt.gca().invert_yaxis() # Invertir el eje Y para que coincida con la imagen
    plt.title("Perfil de intensidad (Brillo por fila)")
    plt.xlabel("Brillo medio")
    plt.ylabel("Posición vertical (píxeles)")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python analizar_placa.py <ruta_imagen>")
    else:
        analizar_imagen(sys.argv[1])