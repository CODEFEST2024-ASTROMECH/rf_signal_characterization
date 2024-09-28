# main.py

import sys
import pandas as pd
import re
import matplotlib.pyplot as plt
from io import StringIO
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMessageBox


class RFSpectrumApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana
        self.setWindowTitle("CODEFEST AD ASTRA 2024 - AstroMech")
        self.setGeometry(100, 100, 400, 200)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Etiqueta de bienvenida
        self.label = QLabel("Bienvenido al CODEFEST AD ASTRA 2024 - AstraMech", self)
        layout.addWidget(self.label)
        
        # Botón para cargar archivo CSV
        self.button = QPushButton("Cargar archivo CSV de señal RF", self)
        self.button.clicked.connect(self.open_file)
        layout.addWidget(self.button)
        
        # Configurando el layout en la ventana
        self.setLayout(layout)
    
    def open_file(self):
        """
        Método para abrir un diálogo y seleccionar un archivo CSV.
        Procesa el archivo y lo divide en tres partes.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "CSV Files (*.csv)", options=options)
        
        if file_name:
            # Leer archivo CSV
            self.process_csv(file_name)
            
    def process_csv(self, file_path):
        """
        Procesar el archivo CSV y dividirlo en las tres partes especificadas.
        """
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Limpiar el csv
        clean_content = re.sub(r";{2,}", "", content)  # Reemplaza secuencias de dos o más ";" por nada
        clean_content = clean_content.replace(',', '.') # Reemplazar comas por puntos para formato decimal adecuado

        # Dividir las tres partes del archivo
        parts = clean_content.split('\n\n')  # Dividir por filas vacías
        
        # Procesar primera parte (información del experimento / metadata)
        self.process_metadata(parts[0])
        
        # Procesar segunda parte (datos de frecuencia y magnitud)
        self.data_instant = self.process_rf_given_time(parts[1])
        self.plot_frequency_magnitude(self.data_instant)

        # Guardar el DataFrame en un archivo CSV
        # Procesar tercera parte (espectrograma)
        self.spectogram = self.process_spectrogram(parts[2])

    def process_metadata(self, text):
        """
        Procesa la primera parte del archivo CSV y almacena la información en un diccionario.
        """
        # Dividir las líneas del texto
        lines = text.splitlines()
        metadata = {}
        
        for line in lines:
            if ';' in line:
                # Dividir cada línea en clave y valor
                parts = line.split(';')
                
                # Caso de que haya tres partes (incluyendo unidades)
                if len(parts) == 3:
                    key, value, unit = parts
                    metadata[key.strip()] = (value.strip(), unit.strip())
                # Caso de dos partes (sin unidades)
                elif len(parts) == 2:
                    key, value = parts
                    metadata[key.strip()] = value.strip()
        
        # Imprimir algunos valores capturados
        print ("Primera parte completa...")
        center_frequency = metadata.get('Center Frequency', 'N/A')
        span = metadata.get('Span', 'N/A')
        ref_level = metadata.get('Ref Level', 'N/A')
        
        print(f"Frecuencia central: {center_frequency} Hz")
        print(f"Span: {span} Hz")
        print(f"Nivel de referencia: {ref_level} dBm")
        
        return metadata
        
    def process_rf_given_time(self, text):
        """
        Procesa la segunda parte del archivo CSV, que contiene los datos de frecuencia y magnitud.
        Devuelve un DataFrame con las columnas 'Frequency [Hz]' y 'Magnitude [dBm]'.
        """        
        # Crear el DataFrame a partir del texto
        data = pd.read_csv(StringIO(text), sep=';', header=0)        
        
        # Asegurarse de que las columnas tengan los nombres correctos y eliminar espacios si es necesario
        data.columns = data.columns.str.strip()
                
        # Convertir las columnas a float (si no están ya en ese formato)
        data['Frequency [Hz]'] = pd.to_numeric(data['Frequency [Hz]'], errors='coerce')
        data['Magnitude [dBm]'] = pd.to_numeric(data['Magnitude [dBm]'], errors='coerce')
        
        print ("Segunda parte completa...")
        return data

    def plot_frequency_magnitude(self, data):
        """
        Grafica los datos de frecuencia vs magnitud.
        """
        # Crear la gráfica
        plt.figure(figsize=(10, 6))
        plt.plot(data['Frequency [Hz]'], data['Magnitude [dBm]'], label='Magnitud de la señal', color='b')
        
        # Configuración del gráfico
        plt.title('Señal de Radiofrecuencia')
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Magnitud [dBm]')
        plt.grid(True)
        plt.legend()
        
        # Mostrar la gráfica
        plt.show()

    def process_spectrogram(self, text):
        """
        Procesa la tercera parte del archivo CSV, despreciando las primeras tres filas y
        devolviendo un DataFrame con la frecuencia como la primera columna y las magnitudes en las siguientes columnas.
        
        Args:
            text (str): El texto correspondiente a la tercera parte del archivo CSV.
            
        Returns:
            DataFrame: Un DataFrame con la columna "Frecuencia [Hz]" y columnas de magnitudes numeradas.
        """
        # Omitir las primeras tres filas y leer el resto
        data = pd.read_csv(StringIO(text), sep=';', header=None, skiprows=3)
        
        # Renombrar las columnas
        column_names = ['Frecuencia [Hz]'] + [str(i) for i in range(data.shape[1] - 1)]
        data.columns = column_names
        
        # Asegurarse de que la columna de frecuencia se convierta a float
        data['Frecuencia [Hz]'] = pd.to_numeric(data['Frecuencia [Hz]'], errors='coerce')
        
        return data

    def filter_dataframe_by_index(df, index):
        """
        Filtra el DataFrame para devolver solo la columna de frecuencia y la columna especificada por el índice.
        
        Args:
            df (DataFrame): El DataFrame original que contiene las columnas.
            index (int): El índice de la columna a filtrar.
            
        Returns:
            DataFrame: Un nuevo DataFrame con dos columnas: "Frecuencia [Hz]" y el valor correspondiente del índice.
        """
        if index < 0 or index >= df.shape[1] - 1:
            raise ValueError(f"Índice fuera de rango. Debe estar entre 0 y {df.shape[1] - 2}.")

        # Crear un nuevo DataFrame con las columnas deseadas
        filtered_df = df.iloc[:, [0, index + 1]]  # index + 1 porque la primera columna es "Frecuencia [Hz]"

        # Renombrar las columnas
        filtered_df.columns = ['Frecuencia [Hz]', f'Columna {index}']

        return filtered_df


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RFSpectrumApp()
    window.show()
    sys.exit(app.exec_())
