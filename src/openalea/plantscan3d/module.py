from openalea.plantgl.gui.qt.QtCore import *
from openalea.plantgl.gui.qt.QtGui import *
from .main_viewer import MainViewer
from .main_window import MainWindow
from .cursor_selector import CursorSelector

class Module:

    def __init__(self, window: MainWindow):
        """
        :param window: The main window.
        """
        self.window: MainWindow = window
        self.viewer: MainViewer = self.window.viewer
        self.cursor: CursorSelector = self.viewer.cursor
        self.isListening = False

    def listenEvents(self, enable=True, highPriority=False):
        """
        Enable or disable event listening.
        :param enable: Enable or disable.
        :param highPriority: If True, the module will be appended at
        the beginning of the queue.
        :return: None
        """
        if enable == self.isListening:
            # No change made
            return

        if enable:
            self.viewer.registerEventListener(self, highPriority)
        else:
            self.viewer.unregisterEventListener(self)

        self.isListening = enable

    def getModule(self, name: str, assertExists: bool=False):
        """
        Return a specific module.
        :param name: The name of the module.
        :param assertExists: If set to True, raise an exception if the module
        does not exist.
        :return: object
        """
        return self.viewer.getModule(name, assertExists)

    def init(self):
        pass

    def closeEvent(self, event: QCloseEvent):
        pass

    def dragEnterEvent(self, event: QDragEnterEvent):
        pass

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        pass

    def dragMoveEvent(self, event: QDragMoveEvent):
        pass

    def dropEvent(self, event: QDropEvent):
        pass

    def keyPressEvent(self, event: QKeyEvent):
        pass

    def keyReleaseEvent(self, event: QKeyEvent):
        pass

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        pass

    def mouseMoveEvent(self, event: QMouseEvent):
        pass

    def mousePressEvent(self, event: QMouseEvent):
        pass

    def mouseReleaseEvent(self, event: QMouseEvent):
        pass

    def wheelEvent(self, event: QWheelEvent):
        pass

    def fastDraw(self):
        pass

    def draw(self):
        pass

    def postDraw(self):
        pass

    def beginSelection(self, point: QPoint):
        pass

    def drawWithNames(self):
        pass

    def endSelection(self, point: QPoint):
        pass

    def postSelection(self, point: QPoint):
        pass
