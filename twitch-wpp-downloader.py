from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *
import os
import sys
import re

def byte_to_mb(bytes):
    return bytes/(1024*1024)

def tamanio_mb(archivo):
    return byte_to_mb(os.path.getsize(archivo))

def tamanio_de_corte(original):
    clip = VideoFileClip(original)
    corte = clip.duration
    tamanio = tamanio_mb(original)
    print(tamanio)
    while tamanio > 99:
        if tamanio > 800:
            corte = corte - 900 
        else:
            corte = corte - 60

        ffmpeg_extract_subclip(original, 0, corte , targetname="temp.mp4")
        tamanio = tamanio_mb("temp.mp4")
        print("CUT: " + str(tamanio))
    return corte

def encontrar_video_original():
    videos = os.listdir()
    for video in videos:
        match = re.search("\.mp4$", video)
        if match:
            print("Video encontrado: ", video)
            return video

if len(sys.argv) < 2:
    print("Usage: twitch-wpp-downloader link/id")
    exit(1)

link = sys.argv[1]
encontrar_video_original()
if os.system("twitch-dl download -q 360p " + link) == 1:
    if os.system("twitch-dl download -q 360p60 " + link) == 1:
        if os.system("twitch-dl download -q 360p50 " + link) == 1:
            if os.system("twitch-dl download -q 360p30 " + link) == 1:
                print("No se pudo encontrar el video")
                exit(1)

video_original = encontrar_video_original()
tamanio_original = VideoFileClip(video_original).duration
offset = tamanio_de_corte(video_original)
base = 0
iteration = 0


while base < tamanio_original:
    ffmpeg_extract_subclip(video_original, base, base + offset , targetname="clip-" + str(iteration) + ".mp4")
    base = base + offset
    iteration = iteration + 1
    


print(os.listdir())
