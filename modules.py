import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import time 
import neurokit2 as nk 
from scipy import signal
import tkinter as tk




def data_loader(df, xcolname, ycolname):
    """Loads data from two headers in csv into a into numpy arrays."""
    x = df.loc[:, xcolname]
    y = df.loc[:, ycolname]
    headers = list(df.columns)
    return x, y 

def preprocessing():
    """ 
    Handles missing/corrupted values, normalization, baseline,
    correction where appropriate and datatype selection
    """
    return

def filters():
    """"filter implementation lpf, hpf, bpf, FIR, IIR filters"""
    return

def analysis(fn,fs):
    """"FFT of signal used to display frequency domain function takes sampling 
    frequency(fs) as an integer and function(fn) as a list"""
    num_points =  len(fn)
    fft_vals = np.fft.rfft(fn)
    fft_freqs = np.fft.rfftfreq(num_points, d=1/fs)
    return fft_freqs, fft_vals

def gui():
    """"Interactive time and frequency domain display for all headers."""
    class GUI:    
        def __init__(self):
            self.window = tk.Tk()
            self.window.title("CSV Plotter")
            self.window.geometry("500x250")

            self.label_1 = tk.Label(self.window, text="CSV File name", font=('Arial', 10))
            self.label_1.pack()
            self.textbox1 = tk.Text(self.window, height=1, font=('Arial', 16))
            self.textbox1.pack(padx=20)


            self.button = tk.Button(self.window, text="Load csv", font=('Arial',10),command=self.show_message)
            self.button.pack(padx=10,pady=10)

        def show_message(self):
            self.filename = self.textbox1.get('1.0', 'end-1c')
            self.window.destroy()

    class GUI2:
        

        def __init__(self):
            self.window = tk.Tk()
            self.window.title("CSV Plotter")
            self.window.geometry("500x250")


            self.label_1 = tk.Label(self.window, text="X-axis Column Name", font=('Arial', 10))
            self.label_1.pack()
            self.click1 = tk.StringVar()
            dropMenu1 = tk.OptionMenu(self.window, self.click1, *headers)
            dropMenu1.pack() 

            self.label_2 = tk.Label(self.window, text="Y-axis Column Name", font=('Arial', 10))
            self.label_2.pack()
            self.click2 = tk.StringVar()
            dropMenu2 = tk.OptionMenu(self.window, self.click2, *headers)
            dropMenu2.pack() 

            datatypes = ["ECG", "Respiration", "IMU","Temperature"]
            self.label_3 = tk.Label(self.window, text="Datatype", font=('Arial', 10))
            self.label_3.pack()
            self.click3 = tk.StringVar()
            dropMenu3 = tk.OptionMenu(self.window, self.click3, *datatypes)
            dropMenu3.pack()    


            self.label_1 = tk.Label(self.window, text="CSV File name", font=('Arial', 10))
            self.label_1.pack()
            self.textbox1 = tk.Text(self.window, height=1, font=('Arial', 16))
            self.textbox1.pack(padx=20)        

            self.button = tk.Button(self.window, text="Load & Plot", font=('Arial',10),command=self.show_message)
            self.button.pack()



        def show_message(self):
            self.xcolname = self.click1.get()
            self.ycolname = self.click2.get()
            self.datatype = self.click3.get()
            self.samplingFreq = int(self.textbox1.get('1.0', 'end-1c'))
            self.window.destroy()  



    gui = GUI()
    gui.window.mainloop()
    df = pd.read_csv(gui.filename)
    headers = df.columns.tolist()


    while(True) : 
        gui = GUI2()
        gui.window.mainloop()

        x, y = data_loader(df, gui.xcolname, gui.ycolname)
        plt.subplot(2, 1, 1)
        plt.xlabel(gui.xcolname)
        plt.ylabel(gui.ycolname)
        plt.title("Time Domain")
        plt.plot(x,y)

        plt.subplot(2, 1, 2)
        fft_freqs, fft_vals = analysis(y, gui.samplingFreq)
        plt.xlabel("Frequency(Hz)")
        plt.ylabel(gui.ycolname)
        plt.title("Frequency Domain")
        plt.plot(fft_freqs ,fft_vals)
        plt.show()
    return


gui()
