from tkinter import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import filedialog
from tkinter.filedialog import *
import numpy as np
import cv2
import xlwt
from xlsxwriter import Workbook
from matplotlib import pyplot as plt
import csv
import os
import pandas as pd
import io
import time
from scipy.signal import find_peaks

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Bye, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def selectOutputDir():
    OutputDir = filedialog.askdirectory(parent=window)
    outputFile = OutputDir+'/outputCSV.csv'
    print(outputFile)
    text0.insert(INSERT, outputFile)
    # return outputFile
    # outputFile = 'C:/Users/Stasy/Desktop/output2FLASH.txt'

def startMeasurenent():
    outputFile = format(text0.get("1.0", 'end-1c'))
    # import time
    # df = pd.DataFrame({'Name': ['Manchester City', 'Real Madrid', 'Liverpool',
    #                             'FC Bayern München', 'FC Barcelona', 'Juventus'],
    #                    'League': ['English Premier League (1)', 'Spain Primera Division (1)',
    #                               'English Premier League (1)', 'German 1. Bundesliga (1)',
    #                               'Spain Primera Division (1)', 'Italian Serie A (1)'],
    #                    'TransferBudget': [176000000, 188500000, 90000000,
    #                                       100000000, 180500000, 105000000]})
    # df.to_excel(outputFile)
    # Camera stream
    fps = 60
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, fps)
    # Video stream (optional)
    # cap = cv2.VideoCapture("videoplayback.mp4")

    # Image crop
    x, y, w, h = 700, 500, 100, 100
    heartbeat_count = 300
    colorRatio_count = 300
    heartbeat_values = [0] * heartbeat_count
    colorRatio = [0] * colorRatio_count
    heartbeat_times = [time.time()] * heartbeat_count

    # Matplotlib graph surface
    fig = plt.figure()
    ax = fig.add_subplot(111)

    f = open(outputFile, 'w', newline='')
    writer = csv.writer(f)
    frameNumber = 0
    testLength = 50
    times = np.linspace(0, 1, testLength)
    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        # img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        crop_img = img[y:y + h, x:x + w]

        # Update the data (4 heartrate)
        # heartbeat_values = heartbeat_values[1:] + [np.average(crop_img)]
        redIntense = np.average(crop_img[:, :, 0])
        greenIntense = np.average(crop_img[:, :, 1])
        colorRatio = colorRatio[1:] + [redIntense / greenIntense]
        colorRatio2log = [redIntense / greenIntense]
        heartbeat_times = heartbeat_times[1:] + [time.time()]
        frameNumber += 1
        print(frameNumber)

        if frameNumber % testLength == 0:
            print('It is a time!')
            pulses = colorRatio[:-testLength-1:-1]
            print(len(pulses))
            peaks = find_peaks(pulses, height=0)
            peak_pos = times[peaks[0]]
            print(peak_pos)
            HR = len(peak_pos)/testLength
            print(HR)

        writer.writerow(colorRatio2log)

        # Draw matplotlib graph to numpy array
        # ax.plot(heartbeat_times, heartbeat_values)
        ax.plot(heartbeat_times, colorRatio)
        fig.canvas.draw()
        plot_img_np = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.cla()

        # Display the frames
        cv2.imshow('Crop', crop_img)
        cv2.imshow('Graph', plot_img_np)
        cv2.imshow('Red', crop_img[:, :, 0])
        cv2.imshow('Green', crop_img[:, :, 1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    f.close()
    cap.release()
    cv2.destroyAllWindows()
    text1.insert(INSERT, 'Готово')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()
    window.geometry('1100x60')
    window.title("flashFiller")

    lbl1 = Label(window, text="Начать измерение")
    lbl1.grid(column=0, row=1)
    lbl0 = Label(window, text="Выбор директории выходного файла")
    lbl0.grid(column=0, row=0)

    text1 = Text(width=7, height=1)
    text1.grid(column=2, row=1, sticky=(W))
    # text0.pack()
    text0 = Text(width=100, height=1)
    text0.grid(column=2, row=0)

    btn1 = Button(window, text="Start!", command=startMeasurenent)
    btn1.grid(column=1, row=1)
    btn0 = Button(window, text="Выбрать", command=selectOutputDir)
    btn0.grid(column=1, row=0)

    window.mainloop()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/