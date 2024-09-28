import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import re


class RFSpectrumApp:
    def __init__(self):
        self.metadata = {}
        self.data_instant = pd.DataFrame()
        self.spectrogram = pd.DataFrame()

    def read_file(self, file_path):
        """
        Lee un archivo CSV, procesa su contenido y muestra cada parte.
        
        Args:
            file_path (str): Ruta del archivo CSV a leer.
        """
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Limpiar el csv
        clean_content = re.sub(r";{2,}", "", content)  # Reemplaza secuencias de dos o más ";" por nada
        clean_content = clean_content.replace(',', '.')  # Reemplazar comas por puntos para formato decimal adecuado

        # Dividir las tres partes del archivo
        parts = clean_content.split('\n\n')  # Dividir por filas vacías
        
        # Procesar cada parte
        self.metadata = self.process_metadata(parts[0])
        self.data_instant = self.process_rf_given_time(parts[1])
        self.spectrogram = self.process_spectrogram(parts[2])
        
        filter = self.filter_dataframe_by_index(self.spectrogram,532)
        self.plot_frequency_magnitude(filter)
        # Mostrar el contenido procesado
        self.display_content()

    def display_content(self):
        """
        Muestra el contenido de cada parte procesada.
        """
        print("Metadata:")
        for key, value in self.metadata.items():
            print(f"{key}: {value}")
        
        print("\nDatos de frecuencia y magnitud:")
        print(self.data_instant.head())
        
        print("\nEspectrograma:")
        print(self.spectrogram.head())

    def process_metadata(self, text):
        """
        Procesa la primera parte del archivo CSV y almacena la información en un diccionario.
        """
        lines = text.splitlines()
        metadata = {}
        
        for line in lines:
            if ';' in line:
                parts = line.split(';')
                
                if len(parts) == 3:
                    key, value, unit = parts
                    metadata[key.strip()] = (value.strip(), unit.strip())
                elif len(parts) == 2:
                    key, value = parts
                    metadata[key.strip()] = value.strip()
        
        return metadata

    def process_rf_given_time(self, text):
        """
        Procesa la segunda parte del archivo CSV, que contiene los datos de frecuencia y magnitud.
        Devuelve un DataFrame con las columnas 'Frequency [Hz]' y 'Magnitude [dBm]'.
        """        
        data = pd.read_csv(StringIO(text), sep=';', header=0)
        data.columns = data.columns.str.strip()
        data['Frequency [Hz]'] = pd.to_numeric(data['Frequency [Hz]'], errors='coerce')
        data['Magnitude [dBm]'] = pd.to_numeric(data['Magnitude [dBm]'], errors='coerce')
        return data

    def plot_frequency_magnitude(self, data):
        """
        Grafica los datos de frecuencia vs magnitud.
        """
        if data.empty:
            print("No hay datos para graficar.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(data['Frecuencia [Hz]'], data['Magnitud [dBm]'], label='Magnitud de la señal', color='b')
        plt.title('Señal de Radiofrecuencia')
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Magnitud [dBm]')
        plt.grid(True)
        plt.legend()
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
        data = pd.read_csv(StringIO(text), sep=';', header=None, skiprows=3)
        column_names = ['Frecuencia [Hz]'] + [str(i) for i in range(data.shape[1] - 1)]
        data.columns = column_names
        data['Frecuencia [Hz]'] = pd.to_numeric(data['Frecuencia [Hz]'], errors='coerce')
        return data

    def filter_dataframe_by_index(self, df, index):
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

        filtered_df = df.iloc[:, [0, index + 1]]
        filtered_df.columns = ['Frecuencia [Hz]', f'Magnitud [dBm]']
        return filtered_df

Class = RFSpectrumApp()
Class.read_file("resources\SPG_001.csv")
