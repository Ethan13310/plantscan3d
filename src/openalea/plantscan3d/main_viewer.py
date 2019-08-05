from openalea.plantgl.gui.qt.QtCore import *
from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.gui.editablectrlpoint import *
from .modules.serial import *
from .file_history import FileHistory
from .plantscan_settings import PlantScanSettings
from .progress_dialog import ProgressDialog
from .backup import *
from .theme_selector import ThemeSelector
from .modules.editor.cursor_selector import CursorSelector
from collections import deque

class MainViewer(QGLViewer):

    # Qt Signals
    undoAvailable = pyqtSignal(bool)
    redoAvailable = pyqtSignal(bool)

    def __init__(self, parent):
        QGLViewer.__init__(self, parent)
        self.setStateFileName('.plantscan3d.xml')

        self.fileHistory = FileHistory(None, None)
        #self.fileHistory = FileHistory(None, self.openFile)
        self.fileHistory.retrieveSettings(PlantScanSettings())

        self.theme = ThemeSelector(self)

        # plantgl basic object
        self.discretizer = Discretizer()
        self.glRenderer = GLRenderer(self.discretizer)
        self.glRenderer.renderingMode = GLRenderer.Dynamic

        try:
            self.glRenderer.setGLFrame(self)
        except:
            print('No text on GL Display')

        self.clippigPlaneEnabled = False
        self.frontVisibility = 0
        self.backVisibility = 1.0

        self.backup = Backup(self)

        self.progressDialog = ProgressDialog(self)
        self.progressDialog.setMinimumDuration(0.75)
        self.progressDialog.setCancelButtonEnabled(False)

        pgl_register_progressstatus_func(self.showProgress)

        # Disable application exit when using Escape
        self.setShortcut(QGLViewer.EXIT_VIEWER, 0)

        self.setAcceptDrops(True)

        self.cursor = CursorSelector(self)

        self.eventListeners = deque()

    def showProgress(self, message: str, percent: float):
        """
        Update the progress dialog values.
        :param message: The message to display.
        :param percent: The current progress, in [0; 100].
        :return: None
        """
        self.progressDialog.setLabelText(message % percent if '%.2f%%' in message else message)
        self.progressDialog.setProgress(percent)

    def closeEvent(self, event: QCloseEvent):
        """
        Close event.
        :param event:
        :return: None
        """
        settings = PlantScanSettings()
        self.fileHistory.setSettings(settings)
        self.theme.save(settings)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            self.openFile(str(url.toLocalFile()))
        self.updateGL()

    def updateTheme(self, theme: str):
        self.theme.set(theme)
        # TODO: Theme update event
        self.updateGL()

    def createBackup(self, name):
        self.backup.make_backup(name)
        self.undoAvailable.emit(True)
        self.redoAvailable.emit(False)
        #self.discardTempInfoDisplay()

    def undo(self):
        if self.backup.restore_backup():
            self.redoAvailable.emit(True)
            self.updateGL()
        else:
            self.undoAvailable.emit(False)

    def redo(self):
        if self.backup.restore_redo():
            self.undoAvailable.emit(True)
            self.updateGL()
        else:
            self.redoAvailable.emit(False)

    def enabledClippingPlane(self, enabled):
        self.clippigPlaneEnabled = enabled
        if self.isVisible():
            self.updateGL()

    def setFrontVisibility(self, value):
        self.frontVisibility = value
        if self.isVisible():
            self.updateGL()

    def setBackVisibility(self, value):
        self.backVisibility = value
        if self.isVisible():
            self.updateGL()

    def init(self):
        """
        Initialize the viewer.
        :return: None
        """
        self.camera().setViewDirection(Vec(0, -1, 0))
        self.camera().setUpVector(Vec(0, 0, 1))

        # Restore theme
        self.theme.restore(PlantScanSettings())

        # Select current theme in the menu bar
        for action in self.mainWindow.themeActionGroup.actions():
            if action.text() == self.theme.getName():
                action.setChecked(True)
                break

        # Init modules
        # TODO: init modules

    def registerEventListener(self, module):
        """
        Register a module as an event listener.
        :param module: The module to register.
        :return: None
        """
        if self.eventListeners.count(module) == 0:
            # The module is not registered yet
            self.eventListeners.append(module)

    def unregisterEventListener(self, module):
        """
        Unregister a module from being an event listener.
        :param module: The module to unregister.
        :return: None
        """
        try:
            self.eventListeners.remove(module)
        except:
            pass

    def leaveEvent(self, event: QEvent):
        """
        Leave event.
        :param event:
        :return: None
        """
        self.cursor.setIsMouseOver(False)

    def enterEvent(self, event: QEvent):
        """
        Enter event.
        :param event:
        :return: None
        """
        self.cursor.setIsMouseOver(True)

    def revolveAroundScene(self):
        self.camera().setRevolveAroundPoint(self.sceneCenter())
