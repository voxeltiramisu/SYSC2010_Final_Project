import numpy as np
from scipy.signal import detrend

class Preprocessor:

    @staticmethod
    def handle_missing(signal):
        """Fill missing values using linear interpolation"""
        signal = np.array(signal, dtype=float)

        nans = np.isnan(signal)
        if np.any(nans):
            signal[nans] = np.interp(
                np.flatnonzero(nans),
                np.flatnonzero(~nans),
                signal[~nans]
            )
        return signal

    @staticmethod
    def normalize(signal):
        """Scale signal between 0 and 1"""
        min_val = np.min(signal)
        max_val = np.max(signal)

        if max_val - min_val == 0:
            raise ValueError("Signal is a straight line") 

        return (signal - min_val) / (max_val - min_val)

    @staticmethod
    def remove_baseline(signal):
        """Remove slow drift"""
        return detrend(signal)

    def preprocess(self, signal):
        """Full preprocessing pipeline"""
        signal = self.handle_missing(signal)
        signal = self.remove_baseline(signal)
        signal = self.normalize(signal)
        return signal
    
if __name__ == '__main__':
    # Unit Testing
    print("Hello World")
    
    # marked as private, google private method