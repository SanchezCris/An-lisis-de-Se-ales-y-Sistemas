#Librerías a utilizar:
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import simpleaudio as sa
import sounddevice as sd
import tkinter as tk
import os
from IPython.display import Audio
from scipy.io import wavfile
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

#Ventana principal:

ventanaP = tk.Tk()
ventanaP.title("Tratamiento de Señales - Grupo No. 1")
ventanaP.geometry("1280x720")

#Métodos y funciones:

def abrirArchivo():
    #Obteniendo Ruta de la entrada de sonido:
    global archivo
    archivo = filedialog.askopenfilename(title = "abrir", initialdir="C:/Downloads", filetypes=(("sound files",".wav"),))

def playFile():
    #Leyendo el archivo wav
    sample_rate, data = wavfile.read(archivo)
    sd.play(data, 44100).wait()

def grabarMIC():
    duracion = 10           #el máximo de tiempo que permite grabar son 10 segundos
    archivoMIC = "grabacion.wav"
    audio = pyaudio.PyAudio()
    stream = audio.open(format = pyaudio.paInt16, channels = 2, rate = 44100, input=True, frames_per_buffer = 1024)
    print("Grabando...") 
    frames = []
    for i in range(0, int(44100/1024*duracion)):
        data = stream.read(1024)
        frames.append(data)
    print("La grabación ha terminado...")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    waveFile=wave.open(archivoMIC, 'wb')
    waveFile.setnchannels(2)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(44100)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

#Botones:

abrirbtn = Button(ventanaP, text = "Explorador de Archivos", command = abrirArchivo, activebackground="red", background="green").place(x=100, y=100)
grabarbtn = Button(ventanaP, text = "Grabar con MIC", command = grabarMIC).place(x=300, y=100)
textbtn = Button(ventanaP, text = "Texto a Sonido").place(x=600, y=100)
playbtn1 = Button(ventanaP, text = "▶ Reproducir", command = playFile).place(x=100, y=150)
playbtn2 = Button(ventanaP).place(x=400, y=150)

ventanaP.mainloop() 