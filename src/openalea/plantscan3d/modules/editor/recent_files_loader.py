from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantscan3d.module import Module

class RecentFilesLoader(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        self.viewer.fileHistory.callfunc = self.tryOpenFile

    def tryOpenFile(self, filePath, fileType=None):
        """
        Try to open a file.
        :param filePath: The path to the file.
        :param fileType: The type of the file.
        :return: None
        """
        try:
            self.openFile(filePath, fileType)
        except AttributeError:
            # Missing module
            QMessageBox.warning(self.window, 'Error', 'Could not open file: a module is missing.')
        except:
            QMessageBox.warning(self.window, 'Error', 'Could not open file: unknown file type.')

    def openFile(self, filePath, fileType=None):
        """
        Open a file.
        :param filePath: The path to the file.
        :param fileType: The type of the file.
        :return: None
        """
        if fileType == 'PTS':
            # Point set
            self.viewer.getModule('pointset_loader').loadFromFile(filePath)
        else:
            # Unknown file type
            raise Exception()

# Export module
export = RecentFilesLoader
