# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 17:38:29 2019

@author: xingg
"""

#from kivy.garden.cefpython import CefBrowser, cefpython
from kivy.app import App

class CefBrowserApp(App):
    def build(self):
        return CefBrowser(start_url='http://kivy.org')

CefBrowserApp().run()

cefpython.Shutdown()