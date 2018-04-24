# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""
import ScraperBriefing
import ScraperMarketBeats
import GUI


class Controller(object):
    """docstring for ClassName"""
    def __init__(self):
        self.briefing = ScraperBriefing.Briefing();
        self.marketbeats = ScraperMarketBeats.MarketBeats();
        self.gui = GUI.GUI();

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def setup(self):
        self.briefing.setup();
        self.marketbeats.setup();
        self.gui.setup(self.briefing, self.marketbeats);
        return True;
        pass

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def execute(self):
        self.gui.execute();
        pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def dispose(self):
        self.briefing.dispose();
        self.marketbeats.dispose();
        self.gui.dispose();
        pass;

def main():
    controller = Controller();
    controller.setup();
    controller.execute();
    controller.dispose();
    pass;

if __name__ == "__main__":
    main();
    pass;
