# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""
import unittest
import GUI

class GUITester(unittest.TestCase):

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def setUp(self):
    	self.gui = GUI.GUI();
    	pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def test_gui_execute(self):
    	self.assertEqual(self.gui.execute(), True, 'Error in GUI execution');
    	pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def tearDown(self):
    	self.gui.dispose();
    	pass;

if __name__ == '__main__':
    unittest.main();
    pass;
