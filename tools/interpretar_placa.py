import cv2
import numpy as np
import sys

def leer_placa(ruta_imagen):
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: No se pudo cargar la imagen.")
        return

    # 1. Definir ROI
    x, y, ancho, alto = 104, 64, 45, 48
    roi = img[y:y+alto, x:x+ancho]

    # 2. Calcular el perfil de mínimos y suavizar
    perfil = np.min(roi, axis=1)
    perfil_suave = cv2.GaussianBlur(perfil.astype(np.float32), (1, 5), 0).flatten()

    # 3. Dividir la ROI en dos zonas para buscar cada línea por separado
    mitad = alto // 2
    
    # Zona superior (Control): de la fila 0 a la mitad
    zona_control = perfil_suave[0:mitad]
    y_control_relativo = np.argmin(zona_control)
    brillo_control = zona_control[y_control_relativo]
    
    # Zona inferior (Test): de la mitad al final
    zona_test = perfil_suave[mitad:]
    y_test_relativo = np.argmin(zona_test) + mitad # Sumamos la mitad para tener la posición real
    brillo_test = perfil_suave[y_test_relativo]

    print(f"\n--- Análisis de la placa ---")
    print(f"Línea Control: pos {y_control_relativo} (brillo: {brillo_control:.1f})")
    print(f"Línea Test:    pos {y_test_relativo} (brillo: {brillo_test:.1f})")

    # Umbral de detección
    UMBRAL_RAYA = 110.0 

    hay_control = brillo_control < UMBRAL_RAYA
    hay_test = brillo_test < UMBRAL_RAYA

    if not hay_control:
        print("\nRESULTADO: INVÁLIDO (No se detecta línea de control)")
    elif hay_control and hay_test:
        print("\nRESULTADO: POSITIVO (Dos líneas detectadas)")
    elif hay_control and not hay_test:
        print("\nRESULTADO: NEGATIVO (Solo línea de control detectada)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python leer_placa.py <ruta_imagen>")
    else:
        leer_placa(sys.argv[1])