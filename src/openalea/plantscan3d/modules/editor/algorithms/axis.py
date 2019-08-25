from openalea.plantgl.gui.editablectrlpoint import *
from openalea.plantscan3d.module import Module

class Axis(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        # Menu
        self.window.menu.addSeparator('Points')
        self.actionSwapYZ = self.window.menu.addAction('Points', 'Swap Y and Z')
        self.actionSortZ = self.window.menu.addAction('Points', 'Sort Z')

        self.actionSwapYZ.triggered.connect(self.swapYandZ)
        self.actionSortZ.triggered.connect(self.sortZ)

        # Editor module
        self.editor = self.getModule('pointset_editor', True)

    def swapYandZ(self):
        if not self.editor.checkPointsLoaded():
            return
        self.editor.points.pointList.swapCoordinates(1, 2)
        if self.editor.pointsRep[0].geometry.pointList.getPglId() != self.editor.points.pointList.getPglId():
            self.editor.pointsRep[0].geometry.pointList.swapCoordinates(1, 2)
        self.viewer.updateGL()

    def sortZ(self):
        if not self.editor.checkPointsLoaded():
            return
        self.viewer.createBackup('points')
        self.editor.points.pointList.sortZ()
        self.editor.setPoints(PointSet(self.editor.points.pointList))
        self.viewer.updateGL()

# Module export
export = Axis
