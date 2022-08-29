from tkinter import *
from tkinter import ttk
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import filedialog
from tkinter.filedialog import *

import cv2
import keyboard as keyboard
import numpy as np
import serial
import xlwt
from xlsxwriter import Workbook
from matplotlib import pyplot as plt
import os
import pandas as pd
import io
import time
from scipy.signal import find_peaks
# import pyserial
from serial.tools import list_ports

comlist = list_ports.comports()
connectedPorts = []
chosen_port = "COM1"
lastOpenedPort = ""
ClosePort = 0

ser = serial.Serial(chosen_port, 115200, timeout=1, parity=serial.PARITY_NONE, stopbits=1)

for element in comlist:
    connectedPorts.append(element.device)
print("Connected COM ports: " + str(connectedPorts))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Bye, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def selectOutputDir():
    OutputDir = filedialog.askdirectory(parent=window)
    outputFile = OutputDir + '/outputCSV.csv'
    print(outputFile)
    text0.insert(INSERT, outputFile)


def connect2Arduino():
    global chosen_port, lastOpenedPort
    chosen_port = combobox0.get()
    if chosen_port == "x":
        chosen_port = lastOpenedPort
        # combobox0.select_clear
    ser = serial.Serial(chosen_port, 115200, timeout=1, parity=serial.PARITY_NONE, stopbits=1)
    if ser.isOpen():
        lastOpenedPort = chosen_port
        print("port is opened")
    while True:
        data = ser.readline()[:-2]  # the last bit gets rid of the new-line chars
        print(data)
        if keyboard.is_pressed("x"):
            break
            # ser.close()
    close_COM_port()
    return

def Record():
    OutputDir = filedialog.askdirectory(parent=window)
    outputFile = OutputDir + '/outputCSV.csv'
    print(outputFile)
    text0.insert(INSERT, outputFile)
    # return outputFile
    # outputFile = 'C:/Users/Stasy/Desktop/output2FLASH.txt'


def saveCSV():
    OutputDir = filedialog.askdirectory(parent=window)
    outputFile = OutputDir + '/outputCSV.csv'
    print(outputFile)
    text0.insert(INSERT, outputFile)
    # return outputFile
    # outputFile = 'C:/Users/Stasy/Desktop/output2FLASH.txt'


def startMeasurenent():
    global chosen_port, lastOpenedPort
    chosen_port = combobox0.get()
    if chosen_port == "x":
        chosen_port = lastOpenedPort
        # combobox0.select_clear
    ser = serial.Serial(chosen_port, 115200, timeout=1, parity=serial.PARITY_NONE, stopbits=1)
    if ser.isOpen():
        lastOpenedPort = chosen_port
        print("port is opened")
    while True:
        data = ser.readline()[:-2]  # the last bit gets rid of the new-line chars
        print(data)
        # fig.canvas.draw()
        # plot_img_np = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        # plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # plt.cla()
        if keyboard.is_pressed("x"):
            break
            # ser.close()
    close_COM_port()
    return

        # writer.writerow(colorRatio2log)

        # Draw matplotlib graph to numpy array
        # ax.plot(heartbeat_times, heartbeat_values)
        # ax.plot(heartbeat_times, colorRatio)
        fig.canvas.draw()
        plot_img_np = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.cla()

    # f.close()
    # text1.insert(INSERT, 'Готово')


def close_COM_port():
    ser.close()
    global ClosePort
    ClosePort = 1
    if (not (ser.isOpen())):
        print("port is closed")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()
    window.geometry('1100x600')
    window.title("Serial logger")

    lbl0 = Label(window, text="Выбор директории выходного файла")
    lbl0.grid(column=0, row=0)
    lbl1 = Label(window, text="Выбор COM порта")
    lbl1.grid(column=0, row=1)
    lbl2 = Label(window, text="Начать измерение")
    lbl2.grid(column=0, row=2)
    lbl3 = Label(window, text="Начать запись")
    lbl3.grid(column=0, row=3)
    lbl4 = Label(window, text="Сохранить CSV")
    lbl4.grid(column=0, row=4)
    lbl5 = Label(window, text="Ratio, A.U.")
    lbl5.grid(column=1, row=5)
    lbl5 = Label(window, text="T, Celsius")
    lbl5.grid(column=1, row=6)

    text0 = Text(width=100, height=1)
    text0.grid(column=2, row=0)
    text1 = Text(width=20, height=1)
    text1.grid(column=2, row=3, sticky=W)
    text2 = Text(width=10, height=1)
    text2.grid(column=2, row=4, sticky=W)
    # text0.pack()

    btn0 = Button(window, text="Выбрать", command=selectOutputDir)
    btn0.grid(column=1, row=0, sticky=W)
    btn1 = Button(window, text="Подключение", command=connect2Arduino)
    btn1.grid(column=2, row=1, sticky=W)
    btn2 = Button(window, text="Измерение", command=startMeasurenent)
    btn2.grid(column=1, row=2, sticky=W)
    btn3 = Button(window, text="Запись", command=Record)
    btn3.grid(column=1, row=3, sticky=W)
    btn4 = Button(window, text="Сохранить", command=saveCSV)
    btn4.grid(column=1, row=4, sticky=W)
    btn5 = Button(window, text="Закрыть порт", command=close_COM_port)
    btn5.grid(column=3, row=1)

    # combobox = ttk.Combobox(window, values=connectedPorts)
    combobox0 = ttk.Combobox(window, values=connectedPorts)
    combobox0.grid(column=1, row=1)
    # combobox0.current(1)

    window.mainloop()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
