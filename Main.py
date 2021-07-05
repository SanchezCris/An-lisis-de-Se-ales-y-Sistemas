#from operator import length_hint
#from wave import Wave_write
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
#import simpleaudio as sa
import sounddevice as sd
import soundfile as sf
import tkinter as tk
import scipy.io.wavfile as waves
#from scipy.io import wavfile
import pygame
import winsound
#import pandas as pd
#import math
#import contextlib
#import librosa
import scipy.fftpack as fourier
from numpy import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox 
#from librosa import *
#from scipy.fftpack import  fft, ifft#from IPython.display import Audio

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


def transFourier():
    #LEYENDO LA SEÑAL DE ENTRADA

    freqCorte = 2000                                #Frecuencia de corte para el filtro
    data, Fs = sf.read(archivo, dtype='float')      #lectura del audio de entrada
    try:audioM = data[:,0]                          #si el audio es estéreo, toma un solo canal de sonido
    except IndexError:audioM = data                 #si el audio es mono, toma el único canal
    L = len(audioM)                                 #longitud del vector que contiene los datos de la señal
    Ts = 0.001                                      #tasa de muestrep
    n = Ts*np.arange(0,L)                           #vector tiempo
    fig,ax = plt.subplots()                         #Grafica 1, señal de entrada dominio del tiempo
    plt.plot(n, audioM)
    plt.xlabel("Tiempo")
    plt.ylabel("Audio")

    #APLICANDO TRANSFORMADA DE FOURIER

    gk=fourier.fft(audioM)
    mGK = abs(gk)
    mGK = mGK[0:L//2]
    F=(Fs/L)*np.arange(0,L//2)
    freqs = fourier.fftfreq(L)*Fs
    fig,bx = plt.subplots()                        #Grafica 2, espectro señal de entrada
    plt.plot(F, mGK)
    plt.xlabel("Frecuencia")
    plt.ylabel("Amplitud")

    #CREACION DEL FILTRO PASABAJO
    fp = []
    for i in range (L):
        if np.abs(freqs[i]) < freqCorte:
            fp.append(1.0)
        else:
            fp.append(0.0)

    #APLICACION DEL FILTRO
    filtrada = []
    for i in range (L):
        producto = fp[i]*gk[i]
        filtrada.append(producto)
    mGK2 = filtrada[0:len(filtrada)//2]
    fig,cx = plt.subplots()                     #Grafica 3, espectro señal de salida
    plt.plot(F, np.abs(mGK2))
    plt.xlabel("Frecuencia")
    plt.ylabel("Amplitud")
    
    #APLICANDO TRANSFORMADA INVERSA DE FOURIER
    m3 = fourier.ifft(filtrada)
    nuevaM3 = np.real(m3)
    fig,dx = plt.subplots()                    #Grafica 4, señal de salida dominio del tiempo
    plt.plot(n, nuevaM3)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    sd.play(nuevaM3, Fs)                      #Reproduce la señal filtrada
    plt.show()
    
def playFile():
    pygame.mixer.music.load(archivo)
    pygame.mixer.music.play(loops=0)

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
def playFileOutput():
    pygame.mixer.music.load(archivo)
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
playbtn7 = Button(ventanaP, text = "▉ Stop", command = transFourier).place(x = 800, y=350)

grupo1 = IntVar() #variable para agrupar a los radio button
rdbtn1 = Radiobutton(ventanaP, text = "Filtro 1", value=1, variable=grupo1, ).place(x=100, y = 200)
#rdbtn2 = Radiobutton(ventanaP, text = "Filtro 2", value=2, variable=grupo1, command= filtroPasaBajo).place(x=100, y = 250)
#rdbtn3 = Radiobutton(ventanaP, text = "Filtro 3", value=3, variable=grupo1, command= filtroPasaBajo).place(x=100, y = 300)
ventanaP.mainloop() 