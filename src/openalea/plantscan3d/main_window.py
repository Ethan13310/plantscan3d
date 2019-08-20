from openalea.plantgl.gui.qt.QtCore import *
from openalea.plantgl.gui.qt.QtGui import *
from . import utils
from .menu_bar import MenuBar
from .module_loader import ModuleLoader
from .plantscan_settings import PlantScanSettings

# UI Compilation
utils.compileUi('main_window.ui')

from . import main_window_ui

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

        # Docks list
        self.docks = {}

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
        settings.setValue('SidebarLeft', self.actionShowLeftSidebar.isChecked())
        settings.setValue('SidebarRight', self.actionShowRightSidebar.isChecked())
        settings.endGroup()

    def restoreWindowState(self):
        """
        Restore the previous window state (position and size).
        :return: None
        """
        try:
            settings = PlantScanSettings()
            settings.beginGroup('Window')

            self.restoreGeometry(settings.value('Geometry'))
            self.restoreState(settings.value('State'))

            self.actionShowLeftSidebar.setChecked(settings.value('SidebarLeft', 'true') != 'false')
            self.actionShowRightSidebar.setChecked(settings.value('SidebarRight', 'true') != 'false')

            settings.endGroup()
        except:
            pass

    def getDockWidget(self, name: str) -> tuple:
        """
        Get the specified dock widget. If it does not exist, it will be created.
        :param name: The name of the dock widget.
        :return: tuple
        """
        name = name.title()
        dock = self.getDockWidgetIfExists(name)

        if dock is None:
            # If it does not exist, we create it
            dock = self.__createDockWidget(name)
            self.docks[name] = dock

        return dock

    def getDockWidgetIfExists(self, name: str):
        """
        Get the specified dock widget. Return None if it does not exist.
        :param name: The name of the dock Widget
        :return: tuple
        """
        name = name.title()
        return self.docks[name] if name in self.docks else None

    def setDockWidgetHeaderColor(self, dock: QDockWidget, color: tuple):
        """
        Set the header background color of a dock widget.
        :param dock: The dock widget.
        :param color: The new color.
        :return: None
        """
        red = str(color[0])
        green = str(color[1])
        blue = str(color[2])

        # Widget CSS
        dock.setStyleSheet(
            'QDockWidget::title {'
            'background-color: rgb(' + red + ',' + green + ',' + blue + ');'
            'padding: 6px 5px;'
            '}')

    def showLeftSidebar(self, visible: bool):
        """
        Show or hide the left sidebar.
        :param visible: Show or hide.
        :return: None
        """
        self.showSideBar(visible, Qt.LeftDockWidgetArea)

    def showRightSidebar(self, visible: bool):
        """
        Show or hide the right sidebar.
        :param visible: Show or hide.
        :return: None
        """
        self.showSideBar(visible, Qt.RightDockWidgetArea)

    def showSideBar(self, visible: bool, dockWidgetArea):
        """
        Show or hide the specific sidebar.
        :param visible: Show or hide.
        :param dockWidgetArea: The area.
        :return: None
        """
        for name in self.docks:
            dock = (self.docks[name])[0]
            if self.dockWidgetArea(dock) == dockWidgetArea:
                dock.setVisible(visible)

    def __createDockWidget(self, name: str) -> tuple:
        """
        Create a QDockWidget.
        :param name: The title of the widget.
        :return: tuple
        """
        dock = QDockWidget(self)
        dock.setMaximumSize(500, 102400)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        dock.setObjectName('dock' + name)
        dock.setWindowTitle(name)

        font = QFont()
        font.setPointSize(12)
        dock.setFont(font)

        self.setDockWidgetHeaderColor(dock, (255, 255, 255))

        # Container widget
        container = QWidget(dock)
        dock.setWidget(container)

        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        return dock, container

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

        self.actionShowLeftSidebar.toggled.connect(self.showLeftSidebar)
        self.actionShowRightSidebar.toggled.connect(self.showRightSidebar)


def main():
    """
    Entry point.
    :return: int
    """
    app = QApplication([])
    window = MainWindow()
    window.loadModules()
    window.restoreWindowState()
    window.show()
    return app.exec()


if __name__ == '__main__':
    main()
