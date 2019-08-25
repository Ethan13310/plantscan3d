from openalea.plantgl.gui.editablectrlpoint import *
from openalea.plantscan3d.module import Module
import openalea.plantscan3d.modules.editor.algorithms.param_dialog as param_dialog

class SoilSelection(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        # Menu
        self.window.menu.addSeparator('Points')
        self.selectSubmenu = self.window.menu.addMenu('Points', 'Select...', True)
        self.selectAction = self.selectSubmenu.addAction('Soil')

        self.selectAction.triggered.connect(self.startSelection)

        # Editor module
        self.editor = self.getModule('pointset_editor', True)

    def startSelection(self):
        """
        Select the soil.
        :return: None
        """
        if not self.editor.checkPointsLoaded():
            return

        centerZ = self.editor.points.pointList.getCenter().z
        minZIndex = self.editor.points.pointList.getZMinIndex()
        minZ = self.editor.points.pointList[minZIndex].z

        maxHeight = minZ + (centerZ - minZ) * 0.5

        dialog = param_dialog.create(self.window, 'Parameterizing the Soil Selection Algorithm', [
            ('Top height percent', int, 10, { 'range': (0, 100) }),
            ('Bottom threshold', float, maxHeight)
        ])

        if dialog.exec():
            # We execute the soil selection algorithm
            topPercent, bottomThreshold = dialog.getParams()
            self.viewer.createBackup('points')
            soilPoints = select_soil(self.editor.points.pointList, IndexArray(0), topPercent, bottomThreshold)
            self.editor.selectPoints(soilPoints)

# Module export
export = SoilSelection
