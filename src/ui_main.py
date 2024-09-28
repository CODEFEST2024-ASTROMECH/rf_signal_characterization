import numpy as np

class SignalAnalysis:
    def __init__(self, data):
        """
        Inicializa la clase con el DataFrame de datos de señal.

        Args:
            data (DataFrame): DataFrame con columnas 'Frequency [Hz]' y 'Magnitude [dBm]'.
        """
        self.data = data

    def get_central_frequency(self):
        """
        Calcula la frecuencia central de la señal.
        
        Returns:
            float: Frecuencia central en Hz.
        """
        # La frecuencia central es la media de las frecuencias
        return np.mean(self.data['Frequency [Hz]'])

    def get_bandwidth(self):
        """
        Calcula el ancho de banda de la señal.

        Returns:
            float: Ancho de banda en Hz.
        """
        # El ancho de banda es la diferencia entre la máxima y mínima frecuencia
        return self.data['Frequency [Hz]'].max() - self.data['Frequency [Hz]'].min()

    def get_average_signal_level(self):
        """
        Calcula el nivel de señal promedio.

        Returns:
            float: Nivel promedio de señal en dBm.
        """
        return np.mean(self.data['Magnitude [dBm]'])

    def get_signal_to_noise_ratio(self):
        """
        Calcula la relación señal-ruido (SNR).
        
        Returns:
            float: Relación señal-ruido en dB.
        """
        # Para calcular SNR, asumimos que el ruido es el nivel mínimo
        signal_power = 10 ** (self.average_signal_level() / 10)  # Convertir dBm a mW
        noise_power = 10 ** (self.data['Magnitude [dBm]'].min() / 10)  # Mínimo nivel en dBm
        snr = 10 * np.log10(signal_power / noise_power)  # Convertir a dB
        return snr