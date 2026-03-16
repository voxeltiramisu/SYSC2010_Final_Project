import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import time 
import neurokit2 as nk 
from scipy import signal
import tkinter as tk




def data_loader(filename, xcolname, ycolname):
    """Loads data from two headers in csv into a into numpy arrays."""
    df = pd.read_csv(filename)
    x = df[xcolname]
    y = df[ycolname]
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

def analysis():
    """"FFT of signal used to display frequency domain function"""
    return

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


            self.label_2 = tk.Label(self.window, text="X-axis Column Name", font=('Arial', 10))
            self.label_2.pack()
            self.textbox2 = tk.Text(self.window, height=1, font=('Arial', 16))
            self.textbox2.pack(padx=20)


            self.label_3 = tk.Label(self.window, text="Y-axis Column Name", font=('Arial', 10))
            self.label_3.pack()
            self.textbox3 = tk.Text(self.window, height=1, font=('Arial', 16))
            self.textbox3.pack(padx=20)
            self.button = tk.Button(self.window, text="Load & Plot", font=('Arial',10),command=self.show_message)
            self.button.pack(padx=10,pady=10)

        def show_message(self):
            self.filename = self.textbox1.get('1.0', 'end-1c')
            self.xcolname = self.textbox2.get('1.0', 'end-1c')
            self.ycolname = self.textbox3.get('1.0', 'end-1c')
            gui.window.destroy()

            
    gui = GUI()
    gui.window.mainloop()
    x, y = data_loader(gui.filename,gui.xcolname, gui.ycolname)

    plt.xlabel(gui.xcolname)
    plt.ylabel(gui.ycolname)
    plt.plot(x,y)
    plt.show()
    return


gui()
