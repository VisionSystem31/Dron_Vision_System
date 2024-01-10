from moviepy.editor import VideoFileClip

def resize_video(input_path, output_path, target_resolution):
    # Cargamos el video
    video = VideoFileClip(input_path)

    # Redimensionamos el video a la resolución deseada (1280x720)
    resized_video = video.resize(target_resolution)

    # Escribimos el nuevo video con la resolución modificada
    resized_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Cierra los clips para liberar memoria
    video.close()
    resized_video.close()

# Ruta del video original
input_video_path = 'DJI_0956.MP4'

# Ruta donde se guardará el video redimensionado
output_video_path = 'DJI_0956_redimensionado.mp4'

# Resolución deseada (1280x720)
target_resolution = (1280, 720)

# Llamamos a la función para redimensionar el video
resize_video(input_video_path, output_video_path, target_resolution)
