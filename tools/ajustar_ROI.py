import cv2
import sys

# Variables globales para guardar las coordenadas
roi_iniciada = False
roi_x1, roi_y1, roi_x2, roi_y2 = -1, -1, -1, -1

def dibujar_rectangulo(event, x, y, flags, param):
    global roi_iniciada, roi_x1, roi_y1, roi_x2, roi_y2
    # Al hacer clic izquierdo, guardamos el punto de inicio
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_iniciada = True
        roi_x1, roi_y1 = x, y
        roi_x2, roi_y2 = x, y
    # Mientras movemos el ratón con el botón pulsado, actualizamos el punto final
    elif event == cv2.EVENT_MOUSEMOVE:
        if roi_iniciada:
            roi_x2, roi_y2 = x, y
    # Al soltar el botón, fijamos el rectángulo
    elif event == cv2.EVENT_LBUTTONUP:
        roi_iniciada = False
        roi_x2, roi_y2 = x, y

def main():
    if len(sys.argv) < 2:
        print("Uso: python ajustar_roi.py <ruta_imagen>")
        sys.exit(1)

    ruta_imagen = sys.argv[1]
    img = cv2.imread(ruta_imagen)
    if img is None:
        print("Error: No se pudo cargar la imagen.")
        sys.exit(1)

    # Crear una copia para no modificar la original
    img_mostrar = img.copy()
    
    nombre_ventana = "Ajustar ROI - Arrastra con el raton y pulsa ENTER"
    cv2.namedWindow(nombre_ventana, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(nombre_ventana, dibujar_rectangulo)

    print("Instrucciones:")
    print("1. Haz clic y arrastra para dibujar un rectangulo sobre la ventana del test.")
    print("2. Si te equivocas, vuelve a dibujar otro.")
    print("3. Cuando estes satisfecho, pulsa la tecla ENTER.")
    print("4. Pulsa ESC para salir sin guardar.")

    while True:
        # Dibujar el rectángulo si se está seleccionando o ya se ha seleccionado
        img_dibujo = img.copy()
        if roi_x1 != -1 and roi_y1 != -1:
            cv2.rectangle(img_dibujo, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 0, 255), 2)

        cv2.imshow(nombre_ventana, img_dibujo)
        tecla = cv2.waitKey(1) & 0xFF

        if tecla == 13: # Tecla ENTER
            if roi_x1 != -1 and roi_y1 != -1:
                # Normalizar coordenadas (por si se dibuja de abajo a arriba)
                x_min, x_max = min(roi_x1, roi_x2), max(roi_x1, roi_x2)
                y_min, y_max = min(roi_y1, roi_y2), max(roi_y1, roi_y2)
                
                print("\n--- Coordenadas de la ROI seleccionada ---")
                print(f"x: {x_min}, y: {y_min}, ancho: {x_max - x_min}, alto: {y_max - y_min}")
                print(f"Para usarlas en OpenCV: img[{y_min}:{y_max}, {x_min}:{x_max}]")
            else:
                print("\nNo has dibujado ninguna region.")
            break
        elif tecla == 27: # Tecla ESC
            print("\nSaliendo sin guardar.")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()