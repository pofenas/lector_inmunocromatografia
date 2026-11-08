import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

def analizar_roi(ruta_imagen):
    # 1. Cargar la imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: No se pudo cargar la imagen.")
        return

    # 2. Aplicar las coordenadas exactas que obtuviste
    x, y, ancho, alto = 104, 64, 45, 48
    roi = img[y:y+alto, x:x+ancho]

    # 3. Calcular el perfil de intensidad
    # En lugar del promedio, usamos el valor mínimo de cada fila (el píxel más oscuro)
    # Esto resalta las rayas negras sobre el fondo blanco
    perfil_min = np.min(roi, axis=1)
    
    # Calcular también el promedio para comparar
    perfil_medio = np.mean(roi, axis=1)

    # 4. Graficar los resultados
    plt.figure(figsize=(12, 5))
    
    # Subplot 1: La imagen original y la ROI
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.gca().add_patch(plt.Rectangle((x, y), ancho, alto, fill=False, edgecolor='red', linewidth=2))
    plt.title("Imagen original y ROI")

    # Subplot 2: El perfil de intensidad
    plt.subplot(1, 2, 2)
    
    # Eje Y invertido para que la parte superior de la imagen quede arriba en la gráfica
    eje_y = range(y, y + alto)
    
    plt.plot(perfil_min, eje_y, color='red', label='Mínimo por fila (detecta rayas)')
    plt.plot(perfil_medio, eje_y, color='blue', linestyle='--', label='Promedio por fila')
    
    plt.gca().invert_yaxis()
    plt.title("Perfil de intensidad (Brillo por fila)")
    plt.xlabel("Nivel de gris (0=negro, 255=blanco)")
    plt.ylabel("Posición vertical (píxeles)")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python analizar_roi.py <ruta_imagen>")
    else:
        analizar_roi(sys.argv[1])
        