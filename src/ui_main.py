# ui_main.py

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("RF Signal Analyzer")
        self.setGeometry(200, 200, 400, 300)
        
        # Layout principal
        self.layout = QVBoxLayout()
        
        # Botón para cargar el archivo
        self.label = QLabel("No se ha cargado ningún archivo", self)
        self.button = QPushButton("Cargar archivo CSV", self)
        self.button.clicked.connect(self.load_csv)
        
        # Añadir widgets al layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        
        # Configurar widget central
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
    
    def load_csv(self):
        # Mostrar diálogo para seleccionar archivo CSV
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar archivo CSV", "", "CSV Files (*.csv)", options=options)
        
        if file_name:
            self.label.setText(f"Archivo cargado: {file_name}")
            self.read_csv(file_name)
    
    def read_csv(self, file_path):
        """
        Lee el archivo CSV y grafica la señal de RF.
        """
        # Leer el archivo CSV usando pandas
        data = pd.read_csv(file_path)

        # Limpiar los datos: quitar columnas vacías y NaNs
        data.dropna(axis=1, how='all', inplace=True)  # Eliminar columnas vacías
        data.columns = data.columns.str.strip()  # Eliminar espacios en los nombres de columnas

        # Obtener frecuencias y magnitudes, asegurando que sean numéricas
        frequencies = pd.to_numeric(data['Frequency [Hz]'], errors='coerce').dropna().values
        magnitudes = pd.to_numeric(data['Magnitude [dBm]'], errors='coerce').dropna().values

        # Asegurarse de que ambas series tengan la misma longitud
        min_length = min(len(frequencies), len(magnitudes))
        frequencies = frequencies[:min_length]
        magnitudes = magnitudes[:min_length]

        # Grafica la señal
        self.plot_signal(frequencies, magnitudes)
    
    def plot_signal(self, frequencies, magnitudes):
        """
        Grafica la señal de RF (Magnitud vs Frecuencia).
        """
        plt.figure()
        plt.plot(frequencies, magnitudes, marker='o')
        plt.title("Análisis de la Señal de RF")
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Magnitud (dBm)")
        plt.grid(True)
        plt.show()

# Main app execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
