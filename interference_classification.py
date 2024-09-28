import pandas as pd
from scipy.signal import find_peaks, spectrogram
import numpy as np

class SignalCharacterization:
    am_col = "Amplitud"
    freq_col = "Frecuencia"
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def get_central_frequency(self):
        "Frecuencia central"
        # Indice donde amplitud es máximo
        index_max = self.data[self.am_col].idxmax()
        # Frecuencia con máxima amplitud
        freq_index_max = self.data.loc[index_max, self.freq_col]
        return freq_index_max
    
    def get_noise_level(self):
        "Nivel de ruido"
        # Indice donde la implitud es mínima
        index_min = self.data[self.am_col].idxmin()
        # Amplitud más baja
        amplitude_min = self.data.loc[index_min, self.am_col]
        return amplitude_min
    
    def get_amplitude(self):
        "Amplitud o potencia"
        index_max = self.data[self.am_col].idxmax()
        # Amplitud más grande
        amplitude_max = self.data.loc[index_max, self.am_col]
        return amplitude_max
    
    def get_snr(self):
        "Relación señal-ruido"
        noise_level = self.get_noise_level()
        amplitude = self.get_amplitude()
        return amplitude - noise_level

    def get_bandwidth(self):
        "Ancho de banda"
        reference_level = -self.get_snr/2
        # Encontrar frecuencias que están por encima del nivel de referencia
        band_freqs = self.data[self.data[self.am_col] >= reference_level][self.freq_col]
        bandwidth = band_freqs.max() - band_freqs.min()
        return bandwidth

    def get_modulation(self):
        """
        Detecta el tipo de modulación basado en pulsos y calcula la frecuencia de repetición de pulso (PRF).
        """
        # Primero, hallamos los picos en la magnitud
        peaks, _ = find_peaks(self.magnitude, height=np.mean(self.magnitude))
        
        # Si se encuentran picos, calculamos la PRF
        if len(peaks) > 1:
            # Calculamos la diferencia entre picos consecutivos para obtener los tiempos de los pulsos
            pulse_intervals = np.diff(peaks)  # Intervalos entre picos
            prf = 1 / np.mean(pulse_intervals)  # Frecuencia de repetición de pulso (en Hz)
            
            # Analizamos la forma del pulso
            pulse_shapes = self.magnitude[peaks]  # Amplitudes de los pulsos
            pulse_shape_avg = np.mean(pulse_shapes)
            
            # Clasificamos la forma del pulso (simple)
            if np.all(pulse_shapes > pulse_shape_avg):
                pulse_type = "Pulsos claros"
            else:
                pulse_type = "Pulsos débiles"

            return f"Frecuencia de Repetición de Pulso (PRF): {prf:.2f} Hz, Tipo de pulso: {pulse_type}"
        else:
            return "No se detectaron pulsos."

    def detect_spectral_peaks(self, height=None, distance=None):
        """
        Detecta los picos espectrales en la señal.

        Args:
            height (float): La altura mínima de los picos a detectar.
            distance (int): La distancia mínima entre picos.

        Returns:
            DataFrame: Un DataFrame que contiene los picos detectados con sus frecuencias y magnitudes.
        """
        
        # Obtener magnitudes y frecuencias
        magnitudes = self.data['Magnitude [dBm]'].values
        frequencies = self.data['Frequency [Hz]'].values
        
        # Encontrar los picos
        peaks, properties = find_peaks(magnitudes, height=height, distance=distance)

        return " ,".join(frequencies[peaks]) 
        
    def get_crest_factor(self):
        "Determinar el factor de cresta"
        # Amplitud máxima
        amplitude_max = self.get_amplitude()
        rms = amplitude_max * 0.707
        return amplitude_max - rms
