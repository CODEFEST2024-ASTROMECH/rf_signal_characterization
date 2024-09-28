# main.py

import sys
import pandas as pd
import re
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
            try:
                # Leer archivo CSV
                self.process_csv(file_name)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo procesar el archivo: {str(e)}")
    
    def process_csv(self, file_path):
        """
        Procesar el archivo CSV y dividirlo en las tres partes especificadas.
        """
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # Eliminar los ";" que están rodeados por otros ";"
            clean_content = re.sub(r";{2,}", "", content)  # Reemplaza secuencias de dos o más ";" por nada

            # Dividir las tres partes del archivo
            parts = clean_content.split('\n\n')  # Dividir por filas vacías
            
            # Procesar primera parte (información del experimento / metadata)
            self.process_metadata(parts[0])
            
            # Procesar segunda parte (datos de frecuencia y magnitud)
            data_part_two = pd.read_csv(pd.compat.StringIO(parts[1]), sep='\t')
            print("Parte 2 - Frecuencia y Magnitud:")
            print(data_part_two.head())  # Mostrar primeros datos
            
            # Procesar tercera parte (espectrograma)
            data_part_three = pd.read_csv(pd.compat.StringIO(parts[2]), sep='\t')
            print("Parte 3 - Espectrograma:")
            print(data_part_three.head())  # Mostrar primeros datos

        except Exception as e:
            raise Exception(f"Error al procesar el archivo: {str(e)}")
    
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
        center_frequency = metadata.get('Center Frequency', 'N/A')
        span = metadata.get('Span', 'N/A')
        ref_level = metadata.get('Ref Level', 'N/A')
        
        print(f"Frecuencia central: {center_frequency} Hz")
        print(f"Span: {span} Hz")
        print(f"Nivel de referencia: {ref_level} dBm")
        
        return metadata
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RFSpectrumApp()
    window.show()
    sys.exit(app.exec_())
