from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.ptime import time
import pyqtgraph as pg
from functools import reduce

__all__ = ['ValueLabel']

class ValueLabel(QtGui.QLabel):
    """
    QLabel specifically for displaying numerical values.
    Extends QLabel adding some extra functionality:
        - displaying units with si prefix
        - built-in exponential averaging 
    """
    
    def __init__(self, parent=None, suffix='', siPrefix=False, averageTime=0, formatStr=None):
        """
        Arguments:
            *suffix*   (str or None) The suffix to place after the value
            *siPrefix* (bool) Whether to add an SI prefix to the units and display a scaled value
            *averageTime* (float) The length of time in seconds to average values. If this value
                                  is 0, then no averaging is performed. As this value increases
                                  the display value will appear to change more slowly and smoothly.
            *formatStr* (str) Optionally, provide a format string to use when displaying text. The text will 
                              be generated by calling formatStr.format(value=, avgValue=, suffix=)
                              (see Python documentation on str.format)
                              This option is not compatible with siPrefix
        """
        QtGui.QLabel.__init__(self, parent)
        self.values = []
        self.averageTime = averageTime ## no averaging by default
        self.suffix = suffix
        self.siPrefix = siPrefix
        if formatStr is None:
            formatStr = '{avgValue:0.2g} {suffix}'
        self.formatStr = formatStr
    
    def setValue(self, value):
        now = time()
        self.values.append((now, value))
        cutoff = now - self.averageTime
        while len(self.values) > 0 and self.values[0][0] < cutoff:
            self.values.pop(0)
        self.update()
        
    def setFormatStr(self, text):
        self.formatStr = text
        self.update()
        
        
    def averageValue(self):
        return reduce(lambda a,b: a+b, [v[1] for v in self.values]) / float(len(self.values))
        
        
    def paintEvent(self, ev):
        self.setText(self.generateText())
        return QtGui.QLabel.paintEvent(self, ev)
        
    def generateText(self):
        if len(self.values) == 0:
            return ''
        avg = self.averageValue()
        val = self.values[-1][1]
        if self.siPrefix:
            return pg.siFormat(avg, suffix=self.suffix)
        else:
            return self.formatStr.format(value=val, avgValue=avg, suffix=self.suffix)
            