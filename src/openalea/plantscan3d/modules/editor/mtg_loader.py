from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.gui.editablectrlpoint import *
from openalea.plantscan3d.modules.editor.serial import *
from openalea.plantscan3d.module import Module
from openalea.plantgl.all import get_shared_data
import os
import sys
import traceback

class MTGLoader(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        # MTG Editor
        self.editor = self.getModule('mtg_editor', True)

        self.window.menu.addSeparator('File')
        self.actionOpen = self.window.menu.addAction('File', 'Open MTG')
        self.actionSave = self.window.menu.addAction('File', 'Save MTG')
        self.actionSaveAs = self.window.menu.addAction('File', 'Save MTG As...')

        self.window.menu.addSeparator('File')
        self.actionImport = self.window.menu.addAction('File', 'Import MTG')
        self.actionExport = self.window.menu.addAction('File', 'Export MTG')

        self.actionOpen.setShortcut(QKeySequence('Ctrl+O'))
        self.actionSave.setShortcut(QKeySequence('Ctrl+S'))
        self.actionSaveAs.setShortcut(QKeySequence('Ctrl+Shift+S'))

        self.actionSave.setEnabled(False)
        self.actionSaveAs.setEnabled(False)

        # Events
        self.actionOpen.triggered.connect(lambda: self.openFile('MTG', '*.mtg *.bmtg'))
        self.actionImport.triggered.connect(lambda: self.openFile('iMTG', '*.mtg'))

        #self.actionSave.triggered.connect(self.saveFile)
        #self.actionSaveAs.triggered.connect(self.saveAsFile)

    def openFile(self, type: str, extensions: str):
        """
        Display the 'Open MTG File' dialog.
        :param type:
        :param extensions:
        :return: None
        """
        # We open the dialog
        extensions = 'MTG Files (' + extensions + ');;All Files (*.*)'
        filePath = QFileDialog.getOpenFileName(self.window, 'Open MTG file', self.__getLastPath(type), extensions)[0]

        # We open the selected file
        if filePath and self.loadFromFile(filePath):
            self.viewer.fileHistory.add(filePath, type)

    def loadFromFile(self, filePath: str, fromDigit: bool=False) -> bool:
        """
        Load a MTG file.
        :param filePath: The path to the MTG file.
        :param fromDigit:
        :return: bool
        """
        try:
            if os.path.splitext(filePath)[1] == '.bmtg':
                mtg = readfile(filePath)
            else:
                # readable mtg format from openalea.mtg module
                mtg = read_mtg_file(filePath)
                if fromDigit:
                    convertStdMTGWithNode(mtg)
                else:
                    mtg = convertToMyMTG(mtg)

            self.editor.setMTG(mtg, filePath)
            self.editor.modelRep = None
            self.viewer.showEntireScene()
            return True
        except:
            QMessageBox.warning(self.window, 'Error', 'Could not load MTG file.')
            return False

    def __getLastPath(self, type: str):
        """
        Return the path to the last opened/saved file.
        :return: str
        """
        try:
            lastFile = self.viewer.fileHistory.getLastFile(type)
            return os.path.dirname(lastFile) if lastFile else get_shared_data('mtgdata')
        except:
            return None

# Export module
export = MTGLoader
