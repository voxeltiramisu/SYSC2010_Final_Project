import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import time 
import neurokit2 as nk 
from scipy import signal
import tkinter as tk
from scipy.signal import find_peaks
from scipy.signal import detrend
import scipy.signal
from tkinter import ttk


def data_loader(df, xcolname, ycolname):
    """Loads data from two headers in csv into a into numpy arrays."""
    x = df.loc[:, xcolname]
    y = df.loc[:, ycolname]
    return x, y 

def update_plot(x,y,fs):
    plt.clf()
    plt.subplot(2, 1, 1)
    plt.xlabel("time(s)")
    plt.ylabel("Amplitude")
    plt.title("Time Domain")
    plt.plot(x,y)

    plt.subplot(2, 1, 2)
    fft_freqs, fft_vals = analysis(y, fs)
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("Amplitude")
    plt.title("Frequency Domain")
    plt.plot(fft_freqs ,fft_vals)

    plt.subplots_adjust(top=0.9, hspace=0.5)

    plt.show(block=False)  
    
    return None


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
    

    # marked as private, google private method




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
        return SignalAnalysis.compute_rate(signal, fs, 0.6)

    # ------------------------
    # RESPIRATION FEATURES
    # ------------------------
    @staticmethod
    def compute_breathing_rate(signal, fs):

        return SignalAnalysis.compute_rate(signal, fs, 2)

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
            features = self.compute_statistics(signal)
            features["heart_rate_bpm"] = self.compute_heart_rate(signal, fs)

        elif data_type == "Respiration":
            features = self.compute_statistics(signal)
            features["breathing_rate_bpm"] = self.compute_breathing_rate(signal, fs)

        elif data_type == "Temperature":
            features = self.compute_statistics(signal)
            features["trend_slope"] = self.compute_trend(signal)

        elif data_type == "Motion":
            features = self.compute_statistics(signal)
            features["activity_level"] = self.compute_activity(signal)

        return features
    
    

def filters(signal, fc=None, fh=None, order=4, filterType="Lowpass", catagory="IIR", fs=1000):
    """Filter implementation LPF, HPF, BPF for FIR and IIR filters"""

    signal = np.asarray(signal)

    nyq = fs / 2

    if fc is not None:
        fc = fc / nyq

    if fh is not None:
        fh = fh / nyq


    def apply_filter(b, a, signal):
        padlen = 3 * max(len(np.atleast_1d(a)), len(np.atleast_1d(b)))

        if len(signal) > padlen:
            return scipy.signal.filtfilt(b, a, signal)
        else:
            return scipy.signal.lfilter(b, a, signal)

    if catagory == "FIR":

        if filterType == "Lowpass":
            taps = scipy.signal.firwin(order, fc, pass_zero="lowpass")
            filtered = apply_filter(taps, 1.0, signal)

        elif filterType == "Highpass":
            taps = scipy.signal.firwin(order, fc, pass_zero="highpass")
            filtered = apply_filter(taps, 1.0, signal)

        elif filterType == "Bandpass":
            taps = scipy.signal.firwin(order, [fc, fh], pass_zero="bandpass")
            filtered = apply_filter(taps, 1.0, signal)

        else:
            raise ValueError("Invalid filterType")


    elif catagory == "IIR":

        if filterType == "Lowpass":
            b, a = scipy.signal.butter(order, fc, btype="low")
            filtered = apply_filter(b, a, signal)

        elif filterType == "Highpass":
            b, a = scipy.signal.butter(order, fc, btype="high")
            filtered = apply_filter(b, a, signal)

        elif filterType == "Bandpass":
            b, a = scipy.signal.butter(order, [fc, fh], btype="band")
            filtered = apply_filter(b, a, signal)

        else:
            raise ValueError("Invalid filterType")

    else:
        raise ValueError("Invalid category")

    return (np.arange(len(filtered)) / fs), filtered


def analysis(fn,fs):
    """"FFT of signal used to display frequency domain function takes sampling 
    frequency(fs) as an integer and function(fn) as a list"""
    num_points =  len(fn)
    fft_vals = np.fft.rfft(fn)
    fft_vals = np.abs(fft_vals) / num_points

    fft_freqs = np.fft.rfftfreq(num_points, 1/fs)

    return fft_freqs, fft_vals

def gui():
    class App(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            self.title("CSV Plotter")
            self.geometry("500x300")

            container = tk.Frame(self)
            container.pack(side="top", fill="both", expand=True)

            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.frames = {}

            # Store shared data
            self.shared_data = {
                "dataframe": pd.DataFrame(),
                "filename": "",
                "headers": [],
                "xcol": "",
                "ycol": "",
                "xcoldata": [],
                "ycoldata": [],
                "datatype": "",
                "fs": "",
                "filterType": "",
                "filterCategory": "",
                "features": {}
            }

            for F in (GUI, GUI2, GUI3, GUI4):
                frame = F(container, self)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(GUI)

        def show_frame(self, cont):
            frame = self.frames[cont]
            if hasattr(frame, "update_dropdowns"):
                frame.update_dropdowns(None)
            frame.tkraise()

    class GUI(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)

            self.controller = controller

            label = tk.Label(self, text="CSV File Name", font=('Arial', 12))
            label.pack(pady=10)

            self.textbox = tk.Text(self, height=1, font=('Arial', 14))
            self.textbox.pack(padx=20)

            button = tk.Button(self,
                            text="Load CSV",
                            command=self.load_csv)
            button.pack(pady=20)

        def load_csv(self):

            filename = self.textbox.get("1.0", "end-1c")
            self.controller.shared_data["filename"] = filename

            try:
                df = pd.read_csv(filename)
                headers = list(df)

                self.controller.shared_data["dataframe"] = df
                self.controller.shared_data["headers"] = headers
                self.controller.show_frame(GUI2)

            except:
                print("Error loading file")

    class GUI2(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)


            self.controller = controller

            self.click1 = tk.StringVar()
            self.click2 = tk.StringVar()
            self.click3 = tk.StringVar()

            headers = self.controller.shared_data["headers"]

            
            self.label_1 = tk.Label(self, text="X-axis Column Name", font=('Arial', 10))
            self.label_1.pack()
            self.dropdown1 = tk.OptionMenu(self, self.click1, "")
            self.dropdown1.pack()


            self.label_2 = tk.Label(self, text="Y-axis Column Name", font=('Arial', 10))
            self.label_2.pack()
            self.dropdown2 = tk.OptionMenu(self, self.click2, "")
            self.dropdown2.pack()


            self.label_3 = tk.Label(self, text="Datatype", font=('Arial', 10))
            self.label_3.pack()
            datatypes = ["ECG", "Respiration", "IMU", "Temperature"]
            self.dropdown3 = tk.OptionMenu(self, self.click3, *datatypes)
            self.dropdown3.pack()

            label_fs = tk.Label(self, text="Sampling Frequency")
            label_fs.pack()

            self.textbox = tk.Text(self, height=1)
            self.textbox.pack()

            button = tk.Button(self,
                            text="Next",
                            command=self.save_data)
            button.pack(pady=10)
            

            

        def update_dropdowns(self, event):

            headers = self.controller.shared_data["headers"]

            menu1 = self.dropdown1["menu"]
            menu1.delete(0, "end")

            menu2 = self.dropdown2["menu"]
            menu2.delete(0, "end")

            for h in headers:
                menu1.add_command(label=h,
                                command=lambda value=h: self.click1.set(value))

                menu2.add_command(label=h,
                                command=lambda value=h: self.click2.set(value))

        def save_data(self):

            self.controller.shared_data["xcol"] = self.click1.get()
            self.controller.shared_data["ycol"] = self.click2.get()
            self.controller.shared_data["datatype"] = self.click3.get()
            self.controller.shared_data["fs"] = int(self.textbox.get("1.0", "end-1c"))

            df = self.controller.shared_data["dataframe"]
            self.controller.shared_data["xcoldata"], self.controller.shared_data["ycoldata"] = data_loader(self.controller.shared_data["dataframe"], self.controller.shared_data["xcol"], self.controller.shared_data["ycol"])
            self.controller.shared_data["ycoldata"] = Preprocessor.preprocess(Preprocessor,self.controller.shared_data["ycoldata"])
            
            update_plot(self.controller.shared_data["xcoldata"],self.controller.shared_data["ycoldata"],self.controller.shared_data["fs"])
            
            self.controller.show_frame(GUI3)

    class GUI3(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller

            label = tk.Label(self, text="Filter Selection", font=('Arial', 12))
            label.pack(pady=10)

            filterTypes = ["Highpass", "Lowpass", "Bandpass"]
            self.click1 = tk.StringVar()
            dropMenu1 = tk.OptionMenu(self, self.click1, *filterTypes)
            dropMenu1.pack()

            category = ["IIR", "FIR"]
            self.click2 = tk.StringVar()
            dropMenu2 = tk.OptionMenu(self, self.click2, *category)
            dropMenu2.pack()

            label3 = tk.Label(self, text="f1(Hz)", font=('Arial', 12))
            label3.pack(pady=10)
            self.textbox3 = tk.Text(self, height=1, font=('Arial', 14))
            self.textbox3.pack(padx=20)

            label4 = tk.Label(self, text="f2(Hz)", font=('Arial', 12))
            label4.pack(pady=10)
            self.textbox4 = tk.Text(self, height=1, font=('Arial', 14))
            self.textbox4.pack(padx=20)

            label5 = tk.Label(self, text="filter order", font=('Arial', 12))
            label5.pack(pady=10)
            self.textbox5 = tk.Text(self, height=1, font=('Arial', 14))
            self.textbox5.pack(padx=20)

            button = tk.Button(self,
                            text="Plot & Save",
                            command=self.save_data)
            button.pack(pady=20)

            button1 = tk.Button(self,
                            text="Next",
                            command=self.next_page)
            button1.pack(pady=20)

        def next_page(self):
            self.controller.shared_data["features"] = SignalAnalysis.extract_features(
            SignalAnalysis,
            self.controller.shared_data["ycoldata"], 
            self.controller.shared_data["fs"],
            self.controller.shared_data["datatype"]    
            )
            self.controller.show_frame(GUI4)
                

        def save_data(self):

            self.controller.shared_data["filterType"] = self.click1.get()
            self.controller.shared_data["filterCategory"] = self.click2.get()
            f1 = int(self.textbox3.get("1.0", "end-1c"))
            f2 = int(self.textbox4.get("1.0", "end-1c"))
            order = int(self.textbox5.get("1.0", "end-1c"))
            x,y = filters(
                self.controller.shared_data["ycoldata"],
                f1,
                f2,
                order,
                self.controller.shared_data["filterType"],
                self.controller.shared_data["filterCategory"] ,
                self.controller.shared_data["fs"])

            update_plot(
                x,
                y,
                self.controller.shared_data["fs"]) 
            
            
            print("\nUser Selections")
            print(self.controller.shared_data)

    class GUI4(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller

            title = tk.Label(self, text="Extracted Features", font=('Arial', 14, "bold"))
            title.pack(pady=10)
   
            self.text = tk.Text(self, height=15, width=50)
            self.text.pack(padx=10, pady=10)

            button = tk.Button(self,
                            text="Again?",  
                            command=self.again)
            button.pack(pady=20)

            button1 = tk.Button(self,
                            text="Exit",
                            command=self.controller.destroy)
            button1.pack(pady=20)

        def update_dropdowns(self, event):
            self.text.delete("1.0", "end")

            features = self.controller.shared_data.get("features")
            keylist = list(features.keys())     
            for x in keylist:
                self.text.insert("end", f"{x}: {features[x]} \n")

        def again(self):
            self.controller.show_frame(GUI)

    app = App()
    app.mainloop()
gui()
