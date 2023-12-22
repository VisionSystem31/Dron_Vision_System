import cv2
import os

def extract_frames(video_path, output_folder, every_n_frame):
    # Verifica si la carpeta de salida existe, si no, la crea
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    contador = 0
    while True:
        success, frame = video_capture.read()

        if not success:
            break

        if frame_count % every_n_frame == 0:
            frame_name = f"{output_folder}/frame_{contador:03d}.jpg"
            cv2.imwrite(frame_name, frame)
            contador +=1

        frame_count += 1

    video_capture.release()

# Ruta del video
video_path = 'DJI_0956.MP4'

# Carpeta de salida para los frames
output_folder = 'frames_DJI_0956'

# Extraer cada 15 frames
every_n_frame = 15

# Llama a la función para extraer los frames
extract_frames(video_path, output_folder, every_n_frame)
