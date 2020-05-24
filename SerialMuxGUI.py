import serial
import threading
import time
import queue
import tkinter as tk
from tkinter import ttk


class SerialThread(threading.Thread):
    def __init__(self, this_queue, com_string):
        threading.Thread.__init__(self)
        self.queue = this_queue
        self.com_string = com_string
        self.s = serial.Serial(self.com_string, 9600)

    def run(self):
        time.sleep(0.01)
        while True:
            if self.s.inWaiting():
                text = self.s.readline(self.s.inWaiting())
                self.queue.put(text)

    def write(self, message):
        self.s.write(str.encode('*00T%'))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #tk.Tk.__init__(self)
        self.geometry("1000x600")
        self.frame_label = tk.Frame(self, padx=40, pady=40)
        # Set up first text box
        self.text1 = tk.Text(self.frame_label, wrap='word', height=12, width=120)
        self.frame_label.pack()
        self.text1.pack()
        # Set up second text box
        self.text2 = tk.Text(self.frame_label, wrap='word', height=12, width=120)
        self.frame_label.pack()
        self.text2.pack()
        # Set up first serial port
        self.queue1 = queue.Queue()
        self.thread1 = SerialThread(self.queue1, 'COM11')
        self.thread1.daemon = True
        self.thread1.start()
        self.process_serial1()
        # Set up second serial port
        self.queue2 = queue.Queue()
        self.thread2 = SerialThread(self.queue2, 'COM5')
        self.thread2.daemon = True
        self.thread2.start()
        self.process_serial2()
        # Create the controls
        self.measure_button = ttk.Button(self, text='Measure (M)', command=self.measure)
        self.measure_button.pack(fill='x')
        self.stop_button = ttk.Button(self, text='Stop (S)', command=self.stop)
        self.stop_button.pack(fill='x')
        self.tune_button = ttk.Button(self, text='Tune (T)', command=self.tune)
        self.tune_button.pack(fill='x')
        self.close_button = ttk.Button(self, text='Close (C)', command=self.finished)
        self.close_button.pack(fill='x')

    def process_serial1(self):
        value = True
        while self.queue1.qsize():
            try:
                new = self.queue1.get()
                if self.text1.index(tk.END) == '10.0':
                    self.text1.delete(1.0, 'end')
                self.text1.insert('end', new)
            except queue.Empty:
                pass
        self.after(10, self.process_serial1)

    def process_serial2(self):
        value = True
        while self.queue2.qsize():
            try:
                new = self.queue2.get()
                if self.text2.index(tk.END) == '11.0':
                    self.text2.delete(1.0, 'end')
                self.text2.insert('end', new)
            except queue.Empty:
                pass
        self.after(10, self.process_serial2)

    def measure(self):
        message = b'\x24\x4D\x4D\x2C\x2C\x16\x0D\x0A'
        self.thread1.write(message)
        self.text1.delete(1.0, 'end')
        self.text1.insert('end', message)

    def stop(self):
        message = b'\x24\x4D\x4F\x2C\x2C\x18\x0D\x0A'
        self.thread1.write(message)
        self.text1.delete(1.0, 'end')
        self.text1.insert('end', message)

    def tune(self):
        message = b'\x24\x4D\x54\x2C\x30\x2C\x37\x2C\x30\x30\x31\x32\x2C\x9F\x0D\x0A'
        self.thread1.write(message)
        self.text1.delete(1.0, 'end')
        self.text1.insert('end', message)

    @staticmethod
    def finished():
        app.destroy()


app = App()
app.mainloop()

