import numpy as np
from scipy.signal import find_peaks

class SignalAnalysis:

    # ------------------------
    # BASIC STATISTICS
    # ------------------------
    @staticmethod
    def compute_statistics(signal):
        return {
            "mean": float(np.mean(signal)),
            "std": float(np.std(signal)),
            "rms": float(np.sqrt(np.mean(signal**2))),
            "peak_to_peak": float(np.ptp(signal))
        }

    # ------------------------
    # ECG FEATURES
    # ------------------------
    @staticmethod
    def compute_rate(signal, fs, modifier):
        peaks, _ = find_peaks(signal, distance=fs*modifier)
        
        if len(peaks) < 2:
            return 0
        
        intervals = np.diff(peaks) / fs
        rate = 60 / np.mean(intervals)
        return float(rate)
        
    def compute_heart_rate(signal, fs):
        """
        Estimate heart rate using peak detection
        """
        return 
        
        (signal, fs, 0.6)

    # ------------------------
    # RESPIRATION FEATURES
    # ------------------------
    @staticmethod
    def compute_breathing_rate(self, signal, fs):

        return self.compute_rate(signal, fs, 2)

    # ------------------------
    # TEMPERATURE FEATURES
    # ------------------------
    @staticmethod
    def compute_trend(signal):
        """Slope of signal (trend)"""
        x = np.arange(len(signal))
        slope = np.polyfit(x, signal, 1)[0]
        return float(slope)

    # ------------------------
    # MOTION FEATURES
    # ------------------------
    @staticmethod
    def compute_activity(signal):
        """Activity level using RMS"""
        return float(np.sqrt(np.mean(signal**2)))

    # ------------------------
    # MAIN FEATURE SELECTOR
    # ------------------------
    def extract_features(self, signal, fs, data_type):
        features = {}

        if data_type == "ECG":
            features["heart_rate_bpm"] = self.compute_heart_rate(signal, fs)

        elif data_type == "Respiration":
            features["breathing_rate_bpm"] = self.compute_breathing_rate(signal, fs)

        elif data_type == "Temperature":
            features["trend_slope"] = self.compute_trend(signal)

        elif data_type == "Motion":
            features["activity_level"] = self.compute_activity(signal)

        return features
    
if __name__ == '__main__':
    # Unit Testing
    print("Hello World")
    
# consider consolodating the rate definitions into 1 that processes the same functions and have the functions take the result from it