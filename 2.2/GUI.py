# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""
import tkinter as tk
from tkinter import ttk

class GUI(object):
    """docstring for ClassName"""
    def __init__(self):
        # main window
        self.win = tk.Tk();
        self.win.title('Stocks Ratings Scraper');
        self.win.geometry('500x500+500+200');
        self.win.resizable(0, 0);

        self.__add__menu__();
        self.__add__mainframe__();

        # self.myLabel1 = tk.Label(self.win, text='MarketBeats & Briefing').pack();

        # self.myButton1 = tk.Button(self.win, text='Start', command=self.startPress).pack();

        self.win.mainloop();
        pass;

    def __add__menu__(self):
        # window menu
        menuBar = tk.Menu(self.win);
        self.win.config(menu=menuBar);
        # file menu
        fileMenu = tk.Menu(menuBar, tearoff=0);
        fileMenu.add_command(label='Exit');
        # help menu
        helpMenu = tk.Menu(menuBar, tearoff=0);
        helpMenu.add_command(label='About');
        # add menu to menu bar
        menuBar.add_cascade(label='File', menu=fileMenu);
        menuBar.add_cascade(label='File', menu=helpMenu);
        pass;

    def __add__mainframe__(self):
        # main frame
        mainFrame = ttk.LabelFrame(self.win, text='Briefing & MarketBeats');
        mainFrame.grid(column=0, row=0, sticky='WE', padx=10, pady=10);

        # start label
        startDateLabel = ttk.Label(mainFrame, text='Start Date：').grid(column=1, row=0);
        self.startDate = tk.StringVar();
        startDateEntered = ttk.Entry(mainFrame, width=12, textvariable=self.startDate);
        startDateEntered.grid(column=1, row=1);
        startDateEntered.delete(0, tk.END);
        startDateEntered.insert(0, 'year-mo-da');

        # end label
        endDateLabel = ttk.Label(mainFrame, text='End Date：').grid(column=2, row=0);
        self.endDate = tk.StringVar();
        endDateEntered = ttk.Entry(mainFrame, width=12, textvariable=self.endDate);
        endDateEntered.grid(column=2, row=1);
        endDateEntered.delete(0, tk.END);
        endDateEntered.insert(0, 'year-mo-da');
        pass

    def startPress(self):
        self.myLabel2 = tk.Label(self.win, text=self.startDate.get()).pack();
        pass;


def main():
    gui = GUI();
    pass;

if __name__ == "__main__":
    main();
    pass;