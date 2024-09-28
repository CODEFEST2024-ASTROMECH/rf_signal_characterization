# main.py

import csv
import numpy as np
import matplotlib.pyplot as plt

def read_csv(file_path):
    """
    Función para leer un archivo CSV y retornar los datos como listas.
    """
    frequencies = []
    amplitudes = []
    times = []
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            frequencies.append(float(row['Frecuencia(Hz)']))
            amplitudes.append(float(row['Amplitud(dBm)']))
            times.append(float(row['Tiempo(s)']))
    
    return np.array(frequencies), np.array(amplitudes), np.array(times)

def plot_signal(frequencies, amplitudes):
    """
    Función para graficar la señal de RF (Amplitud vs Frecuencia).
    """
    plt.plot(frequencies, amplitudes)
    plt.title("Análisis de la Señal de RF")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Amplitud (dBm)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Ruta del archivo CSV
    file_path = "resources/spectral_01.csv"
    
    # Leer los datos del CSV
    frequencies, amplitudes, times = read_csv(file_path)
    
    # Graficar la señal de RF
    plot_signal(frequencies, amplitudes)
