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
        win = tk.Tk();
        win.title('Stocks Ratings Scraper');
        win.geometry('500x500+500+200');
        win.resizable(0, 0);

        self.__add__menu__(win);
        self.__add__mainframe__(win);

        # self.myLabel1 = tk.Label(self.win, text='MarketBeats & Briefing').pack();

        # self.myButton1 = tk.Button(self.win, text='Start', command=self.startPress).pack();

        win.mainloop();
        pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def __add__menu__(self, win):
        # window menu
        menuBar = tk.Menu(win);
        win.config(menu=menuBar);
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

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def __add__mainframe__(self, win):
        # main frame
        mainFrame = ttk.LabelFrame(win, text='   Briefing & MarketBeats   ');
        mainFrame.grid(column=0, row=0, sticky='WE', padx=10, pady=10);

        self.__add__start__label__(mainFrame);
        self.__add__end__label__(mainFrame);
        self.__add__file__path__label__(mainFrame);
        
        pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def __add__start__label__(self, mainFrame):
        # start date label
        startDateLabel = ttk.Label(mainFrame, text='Start Date');
        startDateLabel.grid(column=0, row=0, sticky='W', padx=10, pady=10);
        self.startDate = tk.StringVar();
        startDateEntered = ttk.Entry(mainFrame, width=12, textvariable=self.startDate);
        startDateEntered.grid(column=1, row=0, sticky='W');
        startDateEntered.delete(0, tk.END);
        startDateEntered.insert(0, 'year-mo-da');
        pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def __add__end__label__(self, mainFrame):
        # end date label
        endDateLabel = ttk.Label(mainFrame, text='End Date:');
        endDateLabel.grid(column=0, row=1, sticky='W', padx=10, pady=10);
        self.endDate = tk.StringVar();
        endDateEntered = ttk.Entry(mainFrame, width=12, textvariable=self.endDate);
        endDateEntered.grid(column=1, row=1, sticky='W');
        endDateEntered.delete(0, tk.END);
        endDateEntered.insert(0, 'year-mo-da');
        pass


    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def __add__file__path__label__(self, mainFrame):
        # filepahtLable = ttk.Label(mainFrame, text='File path');
        # filepahtLable.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*")))
        # print (filepahtLable.filename)
        pass


    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def startPress(self):
        self.myLabel2 = tk.Label(self.win, text=self.startDate.get()).pack();
        pass;


def main():
    gui = GUI();
    pass;

if __name__ == "__main__":
    main();
    pass;