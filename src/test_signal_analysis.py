# test_signal_analysis.py

import pandas as pd
from ui_main import SignalAnalysis  # Asumiendo que la clase se guarda en signal_analysis.py

# Leer los datos desde el archivo CSV guardado
data = pd.read_csv('resources/processed_data.csv')

# Instanciar la clase SignalAnalysis
signal_analysis = SignalAnalysis(data)

# Calcular y mostrar los parámetros
print(f"1. Frecuencia Central: {signal_analysis.calculate_center_frequency()} Hz")
print(f"2. Ancho de Banda: {signal_analysis.calculate_bandwidth()} Hz")
print(f"3. Amplitud/Potencia: {signal_analysis.calculate_power_level()} dBm")
print(f"4. Identificar tipo de modulación: {signal_analysis.identify_modulation()}")

peaks_df = signal_analysis.detect_spectral_peaks(height=-80, distance=5)
print("5. Picos Espectrales Detectados:")
print(peaks_df)

crest_factor = signal_analysis.calculate_crest_factor()
print(f"6. Crest Factor: {crest_factor:.2f} dB")

bandwidth_occupied = signal_analysis.calculate_bandwidth_occupation(threshold=-80)
print(f"7. Ancho de Banda Ocupado: {bandwidth_occupied} Hz")

prf = signal_analysis.calculate_pulse_repetition_frequency()
print(f"8. Frecuencia de Repetición de Pulsos (PRF): {prf:.2f} Hz")

frequency_drift = signal_analysis.calculate_frequency_drift()
print(f"9. Drift de Frecuencia: {frequency_drift:.2f} Hz")

time_of_occupation = signal_analysis.calculate_time_of_occupation(threshold=-80)
print(f"10. Tiempo de Ocupación: {time_of_occupation:.2f} segundos")