from PyQt5.QtWidgets import *
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QTAgg as NavigationToolbar # haven't tried this yet in PyQt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    '''
    Class to represent the FigureCanvas widget
    '''
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MplWidget(QWidget):
    '''
    Widget promoted and defined in Qt Designer
    '''
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        
# class MplWidget(QWidget):
#     def __init__(self, parent = None):
#         QWidget.__init__(self, parent)
#         self.canvas = MplCanvas()
#         self.mpl_toolbar = NavigationToolbar(self.canvas, self)
#         self.vbl = QVBoxLayout()
#         self.vbl.addWidget(self.canvas)
#         self.vbl.addWidget(self.mpl_toolbar)
#         self.setLayout(self.vbl)
