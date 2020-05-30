#----------------------------------------------------- 
# windowHelpers.py
#
# Created by:   Michael Kuczynski
# Created on:   29-05-2020
#
# Description: Functions for log messages.
#----------------------------------------------------- 

import logging
from PyQt5.QtWidgets import QPlainTextEdit

class LogWidget(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    # Overloaded function from logging
    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def clear(self):
        self.widget.clear()

class LogMessage:
    def __init__(self):
        self.msgType = -1
        self.msgText = ''
        self.msgTypeDict = {
            -1: 'None',
             0: 'Debug',
             1: 'Info',
             2: 'Warning',
             3: 'Error'
        }

    def createLogMsg(self, _msgType, _msgText):
        assert type(_msgType) is int and (_msgType > -2 and _msgType < 4)
        assert type(_msgText) is str

        self.msgType = _msgType
        self.msgText = _msgText

        if self.msgType == -1:
            return
        elif self.msgType == 0:
            logging.debug(self.msgText)
        elif self.msgType == 1:
            logging.info(self.msgText)
        elif self.msgType == 2:
            logging.warning(self.msgText)
        elif self.msgType == 3:
            logging.error(self.msgText)
        
        self.msgType = -1
        self.msgText = ''