from openalea.plantgl.gui.editablectrlpoint import *
from openalea.plantscan3d.module import Module

class Density(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        # Menu
        self.window.menu.addSeparator('Points')
        self.densitySubmenu = self.window.menu.addMenu('Points', 'Density')
        self.actionKDensity = self.densitySubmenu.addAction('K-Density')
        self.actionRDensity = self.densitySubmenu.addAction('R-Density')
        self.densitySubmenu.addSeparator()
        self.actionHistogram = self.densitySubmenu.addAction('Histogram')

        self.actionKDensity.triggered.connect(self.kDensity)
        self.actionRDensity.triggered.connect(self.rDensity)
        self.actionHistogram.triggered.connect(self.histogram)

        # Editor module
        self.editor = self.getModule('pointset_editor', True)

    def kDensity(self):
        pass

    def rDensity(self):
        pass

    def histogram(self):
        pass

# Module export
export = Density
