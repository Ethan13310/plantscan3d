try:
    import openalea.plantscan3d.py2exe_release

    py2exe_release = True
    print('Py2ExeRelease')
except ImportError:
    py2exe_release = False
    print('StdRelease')

from openalea.plantgl.gui.qt.QtCore import *
from openalea.plantgl.gui.qt.QtGui import *

if not py2exe_release:
    from . import ui_compiler as cui

    ldir = os.path.dirname(__file__)
    cui.check_ui_generation(os.path.join(ldir, 'main_window.ui'))

from . import main_window_ui
from .menu_bar import MenuBar
from .module_loader import ModuleLoader
from .plantscan_settings import PlantScanSettings

class MainWindow(QMainWindow, main_window_ui.Ui_MainWindow):

    def __init__(self, parent=None):
        """
        :param parent: Parent window.
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.themeActionGroup = QActionGroup(self)
        self.__setupActions()

        self.viewer.mainWindow = self
        self.viewer.fileHistory.setMenu(self.menuRecentFiles)

        # Default docks size
        self.resizeDocks([self.dockDisplay, self.dockRender], [240, 240], Qt.Horizontal)

        try:
            self.__restoreWindowState()
        except:
            pass

        self.menu = MenuBar(self)
        self.moduleLoader = ModuleLoader('./src/openalea/plantscan3d/modules.conf')

    def loadModules(self):
        """
        Load all modules.
        :return: None
        """
        self.moduleLoader.load(self)

    def closeEvent(self, event: QCloseEvent):
        """
        Close event.
        :param event:
        :return: None
        """
        self.viewer.closeEvent(event)

        if not event.isAccepted():
            # The close event has been rejected, we do not
            # save anything
            return

        settings = PlantScanSettings()
        # Window State
        settings.beginGroup('Window')
        settings.setValue('Geometry', self.saveGeometry())
        settings.setValue('State', self.saveState())
        settings.endGroup()

    def __setupActions(self):
        """
        Connect actions to their respective slots.
        :return: None
        """
        # 'File' menu
        self.actionSaveSnapshot.triggered.connect(self.viewer.saveSnapshot)
        self.actionExit.triggered.connect(self.close)

        # 'Edit' menu
        self.actionUndo.triggered.connect(self.viewer.undo)
        self.actionRedo.triggered.connect(self.viewer.redo)
        self.viewer.undoAvailable.connect(self.actionUndo.setEnabled)
        self.viewer.redoAvailable.connect(self.actionRedo.setEnabled)

        # 'View' menu
        self.themeActionGroup.addAction(self.actionWhiteTheme)
        self.themeActionGroup.addAction(self.actionBlackTheme)

        self.actionWhiteTheme.triggered.connect(lambda: self.viewer.updateTheme('White'))
        self.actionBlackTheme.triggered.connect(lambda: self.viewer.updateTheme('Black'))

    def __restoreWindowState(self):
        """
        Restore the previous previous window state (position and size).
        :return: None
        """
        settings = PlantScanSettings()
        settings.beginGroup('Window')

        self.restoreGeometry(settings.value('Geometry'))
        self.restoreState(settings.value('State'))
        settings.endGroup()


def main():
    """
    Entry point.
    :return: int
    """
    app = QApplication([])
    window = MainWindow()
    window.loadModules()
    window.show()
    return app.exec()


if __name__ == '__main__':
    main()
