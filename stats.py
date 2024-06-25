import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication


class RealTimePlotter:
    def __init__(self):
        """
        Initializes the RealTimePlotter with necessary attributes.
        """
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
        """
        Updates the data of the plot with the given scores and mean scores.

        Parameters
        ----------
        scores : list
            List of scores to be plotted.
        mean_scores : list
            List of mean scores to be plotted.
        """
        self.scores = scores
        self.mean_scores = mean_scores
        self.curve1.setData(self.scores)
        self.curve2.setData(self.mean_scores)

    def run(self):
        """
        Starts the Qt event loop and updates the plot periodically.
        """
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(50)
        self.app.exec_()

    def update(self):
        """
        Updates the curves with the current scores and mean scores.
        """
        self.curve1.setData(self.scores)
        self.curve2.setData(self.mean_scores)


def plot(scores, mean_scores, plotter):
    """
    Updates the plotter with new scores and mean scores.

    Parameters
    ----------
    scores : list
        List of scores to be plotted.
    mean_scores : list
        List of mean scores to be plotted.
    plotter : RealTimePlotter
        An instance of RealTimePlotter that will be updated.
    """
    plotter.update_plot(scores, mean_scores)


def start_plotter(plotter):
    """
    Starts the PyQtGraph application in a new thread.

    Parameters
    ----------
    plotter : RealTimePlotter
        An instance of RealTimePlotter to run the application.
    """
    plotter.run()
