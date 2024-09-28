# test_signal_analysis.py

import pandas as pd
from ui_main import SignalAnalysis  # Asumiendo que la clase se guarda en signal_analysis.py

# Leer los datos desde el archivo CSV guardado
data = pd.read_csv('resources/processed_data.csv')

# Instanciar la clase SignalAnalysis
signal_analysis = SignalAnalysis(data)

# Calcular y mostrar los parámetros
print(f"Frecuencia Central: {signal_analysis.get_central_frequency()} Hz")
print(f"Ancho de Banda: {signal_analysis.get_bandwidth()} Hz")
print(f"Nivel de Señal Promedio: {signal_analysis.get_average_signal_level()} dBm")
print(f"Relación Señal-Ruido: {signal_analysis.get_signal_to_noise_ratio()} dB")
