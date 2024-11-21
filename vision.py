import cv2
import numpy as np
from collections import deque
import time
import os

min_threshold = 10                      # Valores para filtrar el detector.
max_threshold = 200
min_area = 100
min_circularity = 0.3
min_inertia_ratio = 0.5

counter = 0                             # Contador para manejar FPS.
readings = deque(maxlen=10)             # Lecturas recientes de número de pips.
current_number = None                   # Número actual detectado.
last_detected_time = None               # Tiempo de la última detección del número.
number_written = False                  # Indica si el número actual ha sido escrito en el archivo.

def vision_loop():
    global current_number, counter, readings, last_detected_time, number_written

    cap = cv2.VideoCapture(0)  # '0' es el ID de la webcam.
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return

    # Configurar el detector de blobs una sola vez fuera del bucle.
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByCircularity = True
    params.filterByInertia = True
    params.minThreshold = min_threshold
    params.maxThreshold = max_threshold
    params.minArea = min_area
    params.minCircularity = min_circularity
    params.minInertiaRatio = min_inertia_ratio

    detector = cv2.SimpleBlobDetector_create(params)

    while True:
        ret, im = cap.read()
        if not ret:
            print("Error al capturar el frame de la cámara")
            continue

        keypoints = detector.detect(im)

        # Dibujar keypoints en el frame.
        im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow("Dice Reader", im_with_keypoints)

        if counter % 10 == 0:
            reading = len(keypoints)
            readings.append(reading)

            # Comprobar si las últimas 3 lecturas son consistentes y diferentes de cero.
            if (len(readings) >= 3 and readings[-1] == readings[-2] == readings[-3]
                    and readings[-1] != 0):
                new_number = readings[-1]

                if new_number != current_number:
                    # El número ha cambiado.
                    current_number = new_number
                    number_written = False  # Necesitamos escribir el nuevo número.
                    print(f"Número detectado: {current_number}")

                # Actualizamos el tiempo de la última detección.
                last_detected_time = time.time()
            else:
                # Las lecturas no son consistentes o son cero.
                if last_detected_time is None:
                    # No hacemos nada.
                    pass
                else:
                    # Verificar si han pasado más de 5 segundos desde la última detección válida.
                    elapsed_time = time.time() - last_detected_time
                    if elapsed_time > 5:
                        if current_number is not None:
                            # Han pasado más de 5 segundos sin detección válida.
                            current_number = None
                            last_detected_time = None
                            number_written = False  # Necesitamos eliminar el archivo.
                            print("No se detecta número durante 5 segundos, número expirado.")

            # Gestionar la escritura en el archivo solo si es necesario.
            if not number_written:
                if current_number is not None:
                    # Escribir el número actual en el archivo.
                    with open('current_number.txt', 'w') as f:
                        f.write(str(current_number))
                    print(f"Número actualizado en el archivo: {current_number}")
                else:
                    # Eliminar el archivo si no hay número válido.
                    if os.path.exists('current_number.txt'):
                        os.remove('current_number.txt')
                    print("Archivo eliminado, no hay número válido.")
                number_written = True  # Evitar escrituras innecesarias.

        counter += 1

        if cv2.waitKey(1) & 0xFF == 27:  # Presiona [Esc] para salir.
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    vision_loop()
