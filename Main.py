from wave import Wave_write
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
#import simpleaudio as sa
#import sounddevice as sd
import tkinter as tk
import scipy.io.wavfile as waves
import pygame
import math
import contextlib
#from IPython.display import Audio
from scipy import fftpack
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

#Ventana principal:

ventanaP = tk.Tk()
ventanaP.title("Tratamiento de Señales - Grupo No. 1")
ventanaP.geometry("1280x720")
pygame.mixer.init()

#Métodos y funciones:

def abrirArchivo():
    #Obteniendo Ruta de la entrada de sonido:
    global archivo
    archivo = filedialog.askopenfilename(title = "abrir", initialdir="C:/Downloads", filetypes=(("sound files",".wav"),))

def graficarSeñalEntrada():
    #global onda
    #global muestreo
    muestreo, onda = waves.read(archivo)
    longitud = np.shape(onda)
    canal1 = onda[:, 0].copy()
    plt.plot(canal1)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.show()

def playFile():
    pygame.mixer.music.load(archivo)
    pygame.mixer.music.play(loops=0)
    filtroPasaBajo()

def stopFile():
    pygame.mixer.music.stop()

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

"""
s=grupo1.get()
    if s==1: messagebox.showinfo(title="Diagnostico", message = "seleccionaste: Pasa BAjo")
    if s==2: messagebox.showinfo(title="Diagnostico", message = "seleccionaste: Pasa Alto")
    if s==3: messagebox.showinfo(title="Diagnostico", message = "seleccionaste: Pasa Banda")
"""
def filtroPasaBajo():
    muestreo, onda = waves.read(archivo)
    longitud = np.shape(onda)
    canal1 = onda[:, 0].copy()
    t=np.linspace(0,2,len(canal1),False)
    #APLICANDO LA TRANSFORMADA DE FOURIER
    S1 = fftpack.fft(canal1)
    S1mod = np.abs(S1) 
    S1arg = np.angle(S1)
    freqs = fftpack.fftfreq(len(canal1))*muestreo
    #CREACION DEL FILTRO PASABAJO
    fp = []
    for i in range (len(canal1)):
        if np.abs(freqs[i]) < 2000:
            fp.append(1.0)
        else:
            fp.append(0.0)
    S1filt = np.multiply(fp, S1)
    S1filtmod = np.abs(S1filt)
    S1filtarg = np.angle(S1filt)
    #CREACION DE LA NUEVA SEÑAL

    nueva = fftpack.ifft(S1filt)
    NUEVA = np.real(nueva)

    #plt.plot(t, NUEVA)
    #plt.xlabel('Tiempo')
    #plt.ylabel('Amplitud')
    #plt.show()
    global rutaSalida
    Wave_write('Nuevo-Anuel-RHLM2.wav', muestreo, NUEVA)
    rutaSalida = wave.open('Nuevo-Anuel-RHLM2.wav', 'r')
    messagebox.showinfo(title="Diagnostico", message = "seleccionaste: Pasa Bajo" + rutaSalida)
      
def playFileOutput():
    pygame.mixer.music.load(rutaSalida)
    pygame.mixer.music.play(loops=0)
#Botones:

abrirbtn = Button(ventanaP, text = "Explorador de Archivos", command = abrirArchivo, activebackground="red", background="green").place(x=100, y=100)
grabarbtn = Button(ventanaP, text = "Grabar con MIC", command = grabarMIC).place(x=300, y=100)
textbtn = Button(ventanaP, text = "Texto a Sonido").place(x=600, y=100)
playbtn1 = Button(ventanaP, text = "▶ Entrada 1", command = playFile).place(x=100, y=150)
playbtn2 = Button(ventanaP, text = "▶ Entrada 2").place(x=300, y=150)
playbtn3 = Button(ventanaP, text = "▶ Entrada 3").place(x=500, y=150)
playbtn4 = Button(ventanaP, text = "▶ Salida 1", command = playFileOutput).place(x=100, y=350)
playbtn5 = Button(ventanaP, text = "▶ Salida 2").place(x=300, y=350)
playbtn6 = Button(ventanaP, text = "▶ Salida 3").place(x=500, y=350)
playbtn7 = Button(ventanaP, text = "▉ Stop", command = graficarSeñalEntrada).place(x = 800, y=350)

grupo1 = IntVar() #variable para agrupar a los radio button
rdbtn1 = Radiobutton(ventanaP, text = "Filtro 1", value=1, variable=grupo1, command= filtroPasaBajo).place(x=100, y = 200)
rdbtn2 = Radiobutton(ventanaP, text = "Filtro 2", value=2, variable=grupo1, command= filtroPasaBajo).place(x=100, y = 250)
rdbtn3 = Radiobutton(ventanaP, text = "Filtro 3", value=3, variable=grupo1, command= filtroPasaBajo).place(x=100, y = 300)
ventanaP.mainloop() 