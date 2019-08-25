from openalea.plantgl.gui.qt.QtCore import *
from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.gui.editablectrlpoint import *
from OpenGL.GL import *
from .backup import Backup
from .file_history import FileHistory
from .theme_selector import ThemeSelector
from .cursor_selector import CursorSelector
from .progress_dialog import ProgressDialog
from .plantscan_settings import PlantScanSettings
from collections import deque

class MainViewer(QGLViewer):

    # Qt Signals
    undoAvailable = pyqtSignal(bool)
    redoAvailable = pyqtSignal(bool)

    def __init__(self, parent):
        """
        :param parent: Parent widget.
        """
        QGLViewer.__init__(self, parent)
        self.setStateFileName('.plantscan3d.xml')

        self.fileHistory = FileHistory(None, lambda a, b: None)
        self.fileHistory.retrieveSettings(PlantScanSettings())

        self.theme = ThemeSelector(self)
        self.cursor = CursorSelector(self)
        self.backup = Backup(self)

        self.discretizer = Discretizer()
        self.glRenderer = GLRenderer(self.discretizer)
        self.glRenderer.renderingMode = self.glRenderer.Dynamic

        try:
            self.glRenderer.setGLFrame(self)
        except:
            pass

        self.progressDialog = ProgressDialog(self)
        self.progressDialog.setMinimumDuration(0.75)
        self.progressDialog.setCancelButtonEnabled(False)

        pgl_register_progressstatus_func(self.showProgress)

        # Disable application exit when using Escape
        self.setShortcut(QGLViewer.EXIT_VIEWER, 0)
        
        self.setAcceptDrops(True)

        # Listening modules
        self.eventListeners = deque()

    def init(self):
        """
        Initialize the viewer.
        :return: None
        """
        self.camera().setViewDirection(Vec(0, -1, 0))
        self.camera().setUpVector(Vec(0, 0, 1))

        # Restore theme
        self.theme.restore(PlantScanSettings())

        # Select the current theme in the menu bar
        for action in self.mainWindow.themeActionGroup.actions():
            if action.text() == self.theme.getName():
                action.setChecked(True)
                break

        # Init modules
        for module in self.getModules(all=True):
            module.init()

    def getModules(self, all: bool=False, hasMethod: str=None):
        """
        Return listening modules.
        :param all: Return all modules instead of only the listening ones.
        :param hasMethod: Return only modules that have this method.
        :return: list
        """
        allModules = self.mainWindow.moduleLoader.modules
        moduleList = allModules if all else self.eventListeners

        if not hasMethod:
            # No method filter
            return moduleList

        newModuleList = []

        for module in moduleList:
            if callable(getattr(module, hasMethod, None)):
                # The module has the specified method
                newModuleList.append(module)

        return newModuleList

    def getModule(self, name: str, assertExists: bool=False):
        """
        Return a specific module.
        :param name: The name of the module.
        :param assertExists: If set to True, raise an exception if the module
        does not exist.
        :return: object
        """
        allModules = self.mainWindow.moduleLoader.moduleNames
        module = allModules[name] if name in allModules else None

        if assertExists and module is None:
            # The required module does not exist
            raise Exception('Module ' + name + ' not found.')

        return module

    def registerEventListener(self, module, highPriority: bool=False):
        """
        Register a module as an event listener.
        :param module: The module to register.
        :param highPriority: If True, the module will be appended at
        the beginning of the queue.
        :return: None
        """
        if self.eventListeners.count(module) == 0:
            # The module is not registered yet
            if highPriority:
                self.eventListeners.appendleft(module)
            else:
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

    def closeEvent(self, event: QCloseEvent):
        """
        Close event.
        :param event:
        :return: None
        """
        for module in self.getModules(all=True):
            module.closeEvent(event)

        if event.isAccepted():
            # The event has been accepted, we save the different
            # settings and states
            settings = PlantScanSettings()
            self.fileHistory.setSettings(settings)
            self.theme.save(settings)

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

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Drag enter event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.dragEnterEvent(event):
                break

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        """
        Drag leave event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.dragLeaveEvent(event):
                break

    def dragMoveEvent(self, event: QDragMoveEvent):
        """
        Drag move event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.dragMoveEvent(event):
                break

    def dropEvent(self, event: QDropEvent):
        """
        Drop event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.dropEvent(event):
                break

    def keyPressEvent(self, event: QKeyEvent):
        """
        Key press event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.keyPressEvent(event):
                return

        QGLViewer.keyPressEvent(self, event)

    def keyReleaseEvent(self, event: QKeyEvent):
        """
        Key release event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.keyReleaseEvent(event):
                return

        QGLViewer.keyReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """
        Mouse double click event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.mouseDoubleClickEvent(event):
                return

        QGLViewer.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Mouse move event.
        :param event:
        :return: None
        """
        for module in self.getModules():
            if module.mouseMoveEvent(event):
                return

        QGLViewer.mouseMoveEvent(self, event)

    def mousePressEvent(self, event: QMouseEvent):
        """
        Mouse press event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.mousePressEvent(event):
                return

        QGLViewer.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Mouse release event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.mouseReleaseEvent(event):
                return

        QGLViewer.mouseReleaseEvent(self, event)
        self.updateGL()

    def wheelEvent(self, event: QWheelEvent):
        """
        Wheel event event.
        :param event: 
        :return: None
        """
        for module in self.getModules():
            if module.wheelEvent(event):
                return

        QGLViewer.wheelEvent(self, event)

    def fastDraw(self):
        """
        Fast draw event.
        :return: None
        """
        glDisable(GL_LIGHTING)

        for module in self.getModules(all=True):
            module.fastDraw()

    def draw(self):
        """
        Draw event.
        :return: None
        """
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        for module in self.getModules(all=True):
            module.draw()

    def postDraw(self):
        """
        Post draw event.
        :return: None
        """
        for module in self.getModules(all=True):
            module.postDraw()

    def beginSelection(self, point: QPoint):
        """
        Begin selection event.
        :param point:
        :return: None
        """
        for module in self.getModules(all=True):
            if module.beginSelection(point):
                break

    def drawWithNames(self):
        """
        Draw with names event.
        :return: None
        """
        for module in self.getModules(all=True):
            if module.drawWithNames():
                break

    def endSelection(self, point: QPoint):
        """
        End selection event.
        :param point:
        :return: None
        """
        for module in self.getModules(all=True):
            if module.endSelection(point):
                break

    def postSelection(self, point: QPoint):
        """
        Post selection event.
        :param point:
        :return: None
        """
        for module in self.getModules(all=True):
            if module.postSelection(point):
                break

    def createBackup(self, name):
        """
        Create a backup of the current data.
        :param name: The name of the backup.
        :return: None
        """
        try:
            self.backup.make_backup(name)
        except:
            pass

        self.undoAvailable.emit(self.backup.undo_available())
        self.redoAvailable.emit(self.backup.redo_available())

        # Notify modules
        for module in self.getModules(all=True, hasMethod='backupCreateEvent'):
            module.backupCreateEvent()

    def undo(self):
        """
        Undo the last action, if available.
        :return: None
        """
        if self.backup.restore_backup():
            self.redoAvailable.emit(self.backup.redo_available())
            self.undoAvailable.emit(self.backup.undo_available())
            self.updateGL()
        else:
            self.undoAvailable.emit(False)

    def redo(self):
        """
        Redo the last action, if available.
        :return: None
        """
        if self.backup.restore_redo():
            self.redoAvailable.emit(self.backup.redo_available())
            self.undoAvailable.emit(self.backup.undo_available())
            self.updateGL()
        else:
            self.redoAvailable.emit(False)

    def updateTheme(self, theme: str):
        """
        Change the current theme.
        :param theme: The name of the new theme.
        :return: None
        """
        self.theme.set(theme)

        # Notify modules
        for module in self.getModules(all=True, hasMethod='themeUpdateEvent'):
            module.themeUpdateEvent(theme)

        self.updateGL()

    def showProgress(self, message: str, percent: float):
        """
        Update the progress dialog values.
        :param message: The message to display.
        :param percent: The current progress, in [0; 100].
        :return: None
        """
        self.progressDialog.setLabelText(message % percent if '%.2f%%' in message else message)
        self.progressDialog.setProgress(percent)
