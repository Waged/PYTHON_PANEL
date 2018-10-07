#!/usr/bin/python3
# feedback_solution.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import serial
import sys
import glob
from time import sleep
import time

root = Tk()
varSymbol = StringVar(root)
counter = 32  # Below 32 everything in ASCII is gibberish


class Feedback:

    def __init__(self, master):
        master.title('FARMER 21 MQTT Feedback')
        master.resizable(False, False)
        master.configure(background='#e1d8b9')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        self.logo = PhotoImage(file='tour_logo.gif')
        ttk.Label(self.frame_header, image=self.logo).grid(row=0, column=0, rowspan=2)
        ttk.Label(self.frame_header, text='FARMER 21 - Settings Panel', style='Header.TLabel').grid(row=0, column=1)
        ttk.Label(self.frame_header, wraplength=300,
                  text=("We're glad you chose our system   "
                        "Please tell us what settings you thought about the 'MQTT' settings.")).grid(row=1, column=1,
                                                                                                     padx=5)

        ttk.Label(self.frame_header, text='').grid(row=3, column=0)

        ttk.Label(self.frame_header, text=' ').grid(row=4, column=1)

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text='Topic').grid(row=0, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Broker ').grid(row=0, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Username').grid(row=2, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Password').grid(row=2, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='   ').grid(row=4, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Minimum Publish interval (Sec.) ').grid(row=5, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Device Info Publish interval (Min.) ').grid(row=6, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Port Number').grid(row=9, column=0, padx=5, sticky='sw')

        # ttk.Label(self.frame_content, text='Comments:').grid(row=9, column=0, padx=5, sticky='sw')

        self.entry_topic = ttk.Entry(self.frame_content, width=24, font=('Arial', 10))
        self.entry_broker = ttk.Entry(self.frame_content, width=24, font=('Arial', 10))
        self.entry_user = ttk.Entry(self.frame_content, width=24, font=('Arial', 10))
        self.entry_pass = ttk.Entry(self.frame_content, show="*", width=24, font=('Arial', 10))
        self.entry_min_interval = ttk.Entry(self.frame_content, width=24, font=('Arial', 10))
        self.entry_device_interval = ttk.Entry(self.frame_content, width=24, font=('Arial', 10))
        self.entry_port_number = ttk.Entry(self.frame_content, width=24, font=('Arial', 10))
        # self.text_comments = Text(self.frame_content, width=50, height=10, font=('Arial', 10))

        self.entry_topic.grid(row=1, column=0, padx=5)
        self.entry_broker.grid(row=1, column=1, padx=5)
        self.entry_user.grid(row=3, column=0, padx=5)
        self.entry_pass.grid(row=3, column=1, padx=5)
        self.entry_min_interval.grid(row=5, column=1, padx=5)
        self.entry_device_interval.grid(row=6, column=1, padx=5)
        self.entry_port_number.grid(row=9, column=1, padx=5)
        # self.text_comments.grid(row=10, column=0, columnspan=2, padx=5)

        box = ttk.Combobox(self.frame_content, textvariable=varSymbol, state='readonly')
        box['values'] = self.serial_ports()
        box.bind("<<ComboboxSelected>>", self.callbackFunc)
        box.current(0)
        box.grid(column=0, row=11, padx=2, pady=2)

        ttk.Button(self.frame_content, text='Submit',
                   command=self.submit).grid(row=14, column=0, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_content, text='Clear',
                   command=self.clear).grid(row=14, column=1, padx=5, pady=5, sticky='w')

        ttk.Button(self.frame_content, text='Refresh',
                   command=self.refresh_serials).grid(row=11, column=1, padx=5, pady=5, sticky='e')

    def submit(self):
        topic = self.entry_topic.get().strip(' \t\n\r')
        broker = self.entry_broker.get().strip(' \t\n\r')
        user_name = self.entry_user.get().strip(' \t\n\r')
        password = self.entry_pass.get()
        serial_port = varSymbol.get()
        print('topic: {}'.format(topic))
        print('broker: {}'.format(broker))
        print('user: {}'.format(user_name))
        print('password: {}'.format(password))
        print('port: {}'.format(self.entry_port_number.get().strip(' \t\n\r')))
        print(print('serial:'+serial_port))
        # print(serial.__file__)
        serial_me = serial.Serial(serial_port, 9600, timeout=3)
        time.sleep(.2)
        serial_me.write(('{user: '+str(user_name)+',pass:'+str(password)+', broker:'+str(broker)+', topic:'+str(topic)
                         + ', port:'+str(serial_port)).encode())
        # time.sleep(.2)
        time.sleep(.2)
        message = serial_me.readline()
        message_decoded = message.strip().decode('ascii')
        print(message_decoded)
        serial_me.close()
        if message_decoded.upper() == 'DONE':
            messagebox.showinfo(title='Farmer 21 Feedback', message='Data Submitted!')
        else:
            messagebox.showerror(title='Farmer 21 Feedback', message='Failed, Try Again!')

    def callbackFunc(self, event):
        myText = varSymbol.get()
        # print("method is called")
        print(myText)
        # print(self.box.get())

    def refresh_serials(self):
        varSymbol = StringVar(root)
        box = ttk.Combobox(self.frame_content, textvariable=varSymbol, state='readonly')
        box['values'] = self.serial_ports()
        box.current(0)
        box.grid(column=0, row=11, padx=2, pady=2)

    def clear(self):
        self.entry_topic.delete(0, 'end')
        self.entry_broker.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        self.entry_user.delete(0, 'end')

    @staticmethod
    def serial_ports():

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        return result

    def send_via_serial(self):

        serial_me = serial.Serial(varSymbol, 9600, timeout=1)
        serial_me.open()
        serial_me.write('hello from python:')
        serial_me.close()
        # print(serial_me.readline())  # Read the newest output from the Arduino
        # sleep(.1)  # Delay for one tenth of a second
        messagebox.showinfo(title='Farmer 21 Feedback', message='Data Submitted !')
        self.clear()


def main():

    feedback = Feedback(root)
    root.mainloop()


if __name__ == "__main__": main()
