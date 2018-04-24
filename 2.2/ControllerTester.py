# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 15:39:13 2018
Version: python 3.6
@author: MrYanc
"""
import unittest
import Controller

class ControllerTester(unittest.TestCase):

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def setUp(self):
    	self.controller = Controller.Controller();
    	pass;

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def test_controller_execute(self):
    	self.assertEqual(self.controller.execute(), True, 'Error in Controller execution');
    	pass

    '''
    function: 
    input: 
    output: 
    exception: 
    '''
    def tearDown(self):
    	self.controller.dispose();
    	pass;

if __name__ == '__main__':
    unittest.main();
    pass;