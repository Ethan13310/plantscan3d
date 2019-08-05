from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.gui.editablectrlpoint import *
from openalea.plantscan3d.module import Module
from openalea.plantgl.all import get_shared_data
import os

class PointsetLoader(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        self.window.menu.addSeparator('File')
        self.actionImport = self.window.menu.addAction('File', 'Import Pointset')
        self.actionExport = self.window.menu.addAction('File', 'Export Pointset')
        self.actionExport.setEnabled(False)

        self.actionImport.triggered.connect(self.openFile)
        self.actionExport.triggered.connect(self.saveToFile)

    def openFile(self):
        """
        Display the 'Open Pointset File' dialog.
        :return: None
        """
        # We open the dialog
        extensions = 'Pointset Files (*.asc *.xyz *.pwn *.pts *.txt *.bgeom *.ply);;All Files (*.*)'
        filePath = QFileDialog.getOpenFileName(self.window, 'Open pointset file', self.__getLastPath(), extensions)[0]

        if filePath:
            # We open the selected file
            if self.loadFromFile(filePath):
                self.viewer.fileHistory.add(filePath, 'PTS')

    def loadFromFile(self, filePath: str) -> bool:
        """
        Load a pointset file.
        :param filePath: The path to the pointset file.
        :return: bool
        """
        self.viewer.progressDialog.setOneShot(True)

        try:
            scene = Scene(filePath)
        except:
            scene = None
        finally:
            self.viewer.progressDialog.setOneShot(False)

        if scene is None or len(scene) == 0:
            # Invalid data
            QMessageBox.warning(self.window, 'Error', 'Could not read data from: ' + filePath)
            return False

        if not self.__displayScene(scene):
            # The pointset editor module is missing
            QMessageBox.warning(self.window, 'Error', 'Could not display scene: pointset editor module is missing.')
            return False

        self.actionExport.setEnabled(True)
        return True

    def saveToFile(self):
        """
        Save the scene to a file.
        :return: None
        """
        extensions = 'Pointset Files (*.asc *.xyz *.pwn *.pts *.bgeom *.ply)'
        filePath = QFileDialog.getSaveFileName(self.window, 'Save pointset file', self.__getLastPath(), extensions)[0]

        if filePath:
            try:
                Scene([self.viewer.getModule('pointset_editor').points]).save(filePath)
            except:
                QMessageBox.warning(self.window, 'Error', 'Could not save pointset to file.')
            else:
                # Successfully saved
                self.viewer.fileHistory.add(filePath, 'PTS')

    def __getLastPath(self):
        """
        Return the path to the last opened/saved file.
        :return: str
        """
        try:
            lastFile = self.viewer.fileHistory.getLastFile('PTS')
            return os.path.dirname(lastFile) if lastFile else get_shared_data('pointset')
        except:
            return None

    def __displayScene(self, scene: Scene):
        """
        Display the loaded scene.
        :param scene: The scene to display.
        :return: None
        """
        editor = self.viewer.getModule('pointset_editor')

        if editor is None:
            # Missing poinset editor module
            return False

        try:
            points = scene[0].geometry.geometry
            editor.translation = scene[0].geometry.translation
            points.pointList.translate(editor.translation)
        except AttributeError:
            points = scene[0].geometry
            editor.translation = Vector3(0, 0, 0)
            editor.setPoints(points)

        self.viewer.showEntireScene()
        return True

# Export module
export = PointsetLoader
