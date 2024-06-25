import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication

class RealTimePlotter:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(show=True, title="PyQtGraph Real-Time Plot")
        self.plot = self.win.addPlot(title="Training...")
        self.plot.setLabel('left', 'Score')
        self.plot.setLabel('bottom', 'Number of games')
        self.curve1 = self.plot.plot(pen='y')
        self.curve2 = self.plot.plot(pen='r')
        self.scores = []
        self.mean_scores = []

    def update_plot(self, scores, mean_scores):
        self.scores = scores
        self.mean_scores = mean_scores
        self.curve1.setData(self.scores)
        self.curve2.setData(self.mean_scores)

    def run(self):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(50)
        self.app.exec_()

    def update(self):
        self.curve1.setData(self.scores)
        self.curve2.setData(self.mean_scores)

def plot(scores, mean_scores, plotter):
    plotter.update_plot(scores, mean_scores)

# Funkcja do uruchomienia aplikacji PyQtGraph w nowym wątku
def start_plotter(plotter):
    plotter.run()