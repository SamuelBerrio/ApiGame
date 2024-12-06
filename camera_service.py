import cv2
import numpy as np
from collections import deque
import time
import os


# Variables globales
min_threshold = 10
max_threshold = 200
min_area = 100
min_circularity = 0.3
min_inertia_ratio = 0.5

counter = 0
readings = deque(maxlen=10)
current_number = None
last_detected_time = None
number_written = False

# Configuración de la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()

# Configurar el detector de blobs
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


def generate_video():
    global current_number, counter, readings, last_detected_time, number_written

    while True:
        ret, im = cap.read()
        if not ret:
            print("Error al capturar el frame de la cámara")
            continue

        keypoints = detector.detect(im)

        # Dibujar keypoints en el frame.
        im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        if counter % 10 == 0:
            reading = len(keypoints)
            readings.append(reading)

            if (len(readings) >= 3 and readings[-1] == readings[-2] == readings[-3] and readings[-1] != 0):
                new_number = readings[-1]

                if new_number != current_number:
                    current_number = new_number
                    number_written = False
                    print(f"Número detectado: {current_number}")

                last_detected_time = time.time()
            else:
                if last_detected_time is None:
                    pass
                else:
                    elapsed_time = time.time() - last_detected_time
                    if elapsed_time > 5:
                        if current_number is not None:
                            current_number = None
                            last_detected_time = None
                            number_written = False
                            print("No se detecta número durante 5 segundos, número expirado.")

            if not number_written:
                number_written = True

        # Convertir la imagen a formato JPEG y devolverla como una respuesta de video
        ret, jpeg = cv2.imencode('.jpg', im_with_keypoints)
        if not ret:
            continue
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        counter += 1

def get_current_number():
    """Retorna el número actualmente detectado por la cámara"""
    global current_number
    return current_number


