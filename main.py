from tkinter import *
from tkinter import ttk
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import filedialog
from tkinter.filedialog import *

import cv2
import keyboard as keyboard
import numpy as np
import pandas as pd
import serial
from matplotlib import pyplot as plt, ticker
import csv
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
import scipy
# from scipy import diff

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
    # print(text0.get(Text))


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
        # print(data)
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

    # statusClear()
    # text3.insert(INSERT, "recorded")
    chosen_port = combobox0.get()
    if chosen_port == "x":
        chosen_port = lastOpenedPort
        # combobox0.select_clear
    ser = serial.Serial(chosen_port, 115200, timeout=1, parity=serial.PARITY_NONE, stopbits=1)
    if ser.isOpen():
        lastOpenedPort = chosen_port
        print("port is opened")
    dataRed = []
    dataIR = []
    dataT = []
    nSeconds = 1
    nSignals = 3
    nMinutes = 20
    frameRate = 100
    # DataLen = frameRate * nSignals * nSeconds
    DataLen = frameRate * nSignals * nMinutes * 60

    dt = 1
    t = np.arange(0, ((DataLen / nSignals)/100), dt)
    # times = [time.time()] * 50

    fig1 = plt.figure()
    gs1 = fig1.add_gridspec(8, hspace=0)
    axs1 = gs1.subplots(sharex=True, sharey=False)

    fig2 = plt.figure()
    gs2 = fig2.add_gridspec(3, hspace=0)
    axs2 = gs2.subplots(sharex=True, sharey=False)

    # ax1 = fig.add_subplot(411)
    # ax2 = fig.add_subplot(412)
    # ax3 = fig.add_subplot(413)
    # ax4 = fig.add_subplot(414)
    # fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, hspace = 0)

    outputFile = 'C:/Users/user/Desktop/outputCSV.csv'
    f = open(outputFile, 'w', newline='')
    writer = csv.writer(f, delimiter=',')
    i=0
    opticalStart = 0
    while opticalStart == 0:
        line = ser.readline()[:-2]
        str = line.decode()  # convert the byte string to a unicode string
        if (str == ''):
            str = "0"
        print(line)
        if(str[0] == "R"):
            opticalStart = 1
        elif (str[0] == "I"):
            opticalStart = 1
    for i in range(DataLen):

    # while True:
        i+=1
        print(i)
        line = ser.readline()[:-2]  # the last bit gets rid of the new-line chars
        # line2 = ser.readline()[:-2]  # the last bit gets rid of the new-line chars
        str = line.decode()  # convert the byte string to a unicode string
        # string2 = line2.decode()  # convert the byte string to a unicode string
        # print(str)
        if (str == ''):
            str = "0"
        if(str[0] == "R"):

           str = str[1:]
           # print(str)
           numRed = float(str)
           dataRed.append(numRed)
        elif(str[0] == "I"):
           str = str[1:]
           # print(str)
           numIR = float(str)
           dataIR.append(numIR)
        elif(str[0] == "T"):
           str = str[1:]
           # print(str)
           numT = float(str)
           dataT.append(numT)

    close_COM_port()
    minLen = min(len(dataRed), len(dataIR))

    dx = 1
    step = 400
    ratio = np.divide(dataRed[:minLen], dataIR[:minLen])
    ratio_SHORT = []
    dataRed_SHORT = []
    dataIR_SHORT = []
    dataT_SHORT = []
    for i in range(0, minLen, step):
        dataRed_SHORT.append(dataRed[i])
        dataIR_SHORT.append(dataIR[i])
        dataT_SHORT.append(dataT[i])
        ratio_SHORT.append(ratio[i])

    dataRed_Diff = np.diff(dataRed_SHORT)/dx
    dataIR_Diff = np.diff(dataIR_SHORT)/dx
    dataT_Diff = np.diff(dataT_SHORT)/dx
    dataRatio_Diff = np.diff(ratio_SHORT) / dx

    # dataRed_Diff = np.gradient(dataRed, dx)
    # dataIR_Diff = np.gradient(dataIR, dx)
    # dataT_Diff = np.gradient(dataT, dx*1000)


    # writer.writerow(dataRed)[0]
    # writer.writerow(dataIR)[0]
    # writer.writerow(dataT)[0]
    # writer.writerow(data2)
    f.close()

    locator = ticker.LinearLocator(20)

    axs1[0].plot(dataRed_SHORT[2:], color = 'r')
    axs1[0].xaxis.set_major_locator(locator)
    axs1[0].set_xlabel('Time')
    axs1[0].set_ylabel('Red [A.U.]')
    axs1[0].grid(True)

    axs1[1].plot(dataIR_SHORT[2:], color = 'b')
    axs1[1].xaxis.set_major_locator(locator)
    axs1[1].set_xlabel('Time')
    axs1[1].set_ylabel('IR [A.U.]')
    axs1[1].grid(True)

    axs1[2].plot(ratio_SHORT[2:], color = 'g')
    axs1[2].xaxis.set_major_locator(locator)
    axs1[2].set_xlabel('Time')
    axs1[2].set_ylabel('Red / IR')
    axs1[2].grid(True)

    axs1[3].plot(dataT_SHORT[2:], color = 'orange')
    axs1[3].xaxis.set_major_locator(locator)
    axs1[3].set_xlabel('Time')
    axs1[3].set_ylabel('T,C')
    axs1[3].grid(True)

    axs1[4].plot(dataRed_Diff[2:], color = 'r')
    axs1[4].xaxis.set_major_locator(locator)
    axs1[4].set_xlabel('Time')
    axs1[4].set_ylabel('dRed/dt [A.U.]')
    axs1[4].grid(True)

    axs1[5].plot(dataIR_Diff[2:], color = 'b')
    axs1[5].xaxis.set_major_locator(locator)
    axs1[5].set_xlabel('Time')
    axs1[5].set_ylabel('dIR/dt [A.U.]')
    axs1[5].grid(True)

    axs1[6].plot(dataT_Diff[2:], color = 'orange')
    axs1[6].xaxis.set_major_locator(locator)
    axs1[6].set_xlabel('Time')
    axs1[6].set_ylabel('dT/dt')
    axs1[6].grid(True)

    axs1[7].plot(dataRatio_Diff[2:], color = 'g')
    axs1[7].xaxis.set_major_locator(locator)
    axs1[7].set_xlabel('Time')
    axs1[7].set_ylabel('dRatio/dt')
    axs1[7].grid(True)

    plt.show()
    # plt.cla()
    # plt.show(data1)
    # cv2.destroyAllWindows()
    return

# def statusClear():
#     lbl6.config(text=f"recorded")
#     # text3.delete(1.0, END)
#     return

def startMeasurenentHex():
    global chosen_port, lastOpenedPort
    # text3.delete(1.0, END)
    # text3.insert(INSERT, "recorded")
    chosen_port = combobox0.get()
    if chosen_port == "x":
        chosen_port = lastOpenedPort
        # combobox0.select_clear
    ser = serial.Serial(chosen_port, 115200, timeout=1, parity=serial.PARITY_NONE, stopbits=1)
    if ser.isOpen():
        lastOpenedPort = chosen_port
        print("port is opened")
    data1 = []
    plt.xlabel('Time')
    plt.ylabel('Potentiometer Reading')
    plt.title('Potentiometer Reading vs. Time')
    # outputFile = format(text0.get("1.0", 'end-1c'))
    outputFile = 'C:/Users/user/Desktop/outputCSV.csv'
    f = open(outputFile, 'w', newline='')
    writer = csv.writer(f, delimiter=',')
    while True:
        line1 = ser.read(size=2)  # the last bit gets rid of the new-line chars
        line1 = int.from_bytes(line1, byteorder='big', signed=False)
        # string1 = line1.decode()  # convert the byte string to a unicode string
        # if(string1 == ''):
        #     string1 = 0

        # num1 = int(string1)
        print(line1)
        print(type(line1))
        data1.append(line1)
        plt.plot(data1)
        plt.draw()
        writer.writerow([line1])
        # writer.writerow([num2])
        plt.pause(0.01)  # pause
        # fig.canvas.draw()

        # plt.cla()
        if keyboard.is_pressed("x"):
            break
            # ser.close()
    close_COM_port()
    # for value in data:
    # writer.writerow([num])
    f.close()
    return

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

    # lbl0 = Label(window, text="Выбор директории выходного файла")
    # lbl0.grid(column=0, row=0)
    lbl1 = Label(window, text="Выбор COM порта")
    lbl1.grid(column=0, row=0)
    lbl2 = Label(window, text="Начать измерение")
    lbl2.grid(column=0, row=1)
    # lbl3 = Label(window, text="Начать запись")
    # lbl3.grid(column=0, row=3)
    # lbl4 = Label(window, text="Сохранить CSV")
    # lbl4.grid(column=0, row=4)
    # lbl5 = Label(window, text="Ratio, A.U.")
    # lbl5.grid(column=1, row=5)
    # lbl5 = Label(window, text="T, Celsius")
    # lbl5.grid(column=1, row=6)
    # lbl6 = Label(window, text="Status")
    # lbl6.grid(column=3, row=0)

    text0 = Text(width=10, height=1)
    text0.grid(column=2, row=0)
    # text1 = Text(width=20, height=1)
    # text1.grid(column=2, row=3, sticky=W)
    # text2 = Text(width=10, height=1)
    # text2.grid(column=2, row=4, sticky=W)
    # text3 = Text(width=10, height=1)        # status of ending
    # text3.grid(column=3, row=0, sticky=W)
    # text0.pack()

    # btn0 = Button(window, text="Выбрать", command=selectOutputDir)
    # btn0.grid(column=1, row=0, sticky=W)
    # btn1 = Button(window, text="Подключение", command=connect2Arduino)
    # btn1.grid(column=2, row=1, sticky=W)
    btn2 = Button(window, text="Измерение", command=startMeasurenent)
    btn2.grid(column=1, row=1, sticky=W)
    btn6 = Button(window, text="Измерение Hex", command=startMeasurenentHex)
    btn6.grid(column=1, row=2, sticky=W)
    # btn3 = Button(window, text="Запись", command=Record)
    # btn3.grid(column=1, row=3, sticky=W)
    # btn4 = Button(window, text="Сохранить", command=saveCSV)
    # btn4.grid(column=1, row=4, sticky=W)
    # btn5 = Button(window, text="Закрыть порт", command=close_COM_port)
    # btn5.grid(column=3, row=1)

    # combobox = ttk.Combobox(window, values=connectedPorts)
    combobox0 = ttk.Combobox(window, values=connectedPorts)
    combobox0.grid(column=1, row=0)
    # combobox0.current(1)

    window.mainloop()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
