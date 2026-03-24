class DataTypeSelector:
    def __init__(self):
        self.supported_types = ["ECG", "Temperature", "Respiration", "Motion"]

    def validate_type(self, data_type):
        if data_type not in self.supported_types:
            raise ValueError(f"Unsupported data type: {data_type}")
        return True

    def get_default_parameters(self, data_type):
        """
        Returns recommended parameters for each signal type
        """
        self.validate_type(data_type)

        params = {
            "ECG": {
                "fs": 250,  # sampling frequency (Hz)
                "filter": {"type": "bandpass", "low": 0.5, "high": 40}
            },
            "Temperature": {
                "fs": 1,
                "filter": {"type": "lowpass", "cutoff": 0.1}
            },
            "Respiration": {
                "fs": 25,
                "filter": {"type": "bandpass", "low": 0.1, "high": 1}
            },
            "Motion": {
                "fs": 50,
                "filter": {"type": "highpass", "cutoff": 0.5}
            }
        }

        return params[data_type]
    
if __name__ == '__main__':
    # Unit Testing
    print("Hello World")