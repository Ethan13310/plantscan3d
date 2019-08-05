from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.gui.editablectrlpoint import *
from openalea.plantscan3d.module import Module

class PointInfos:

    def __init__(self):
        self.pointWidth = 2
        self.selectedPoints = Index([])

class PointsetEditor(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        self.points = None
        self.pointInfos = PointInfos()
        self.translation = None

    def setPoints(self, points):
        pass

# Module export
export = PointsetEditor
