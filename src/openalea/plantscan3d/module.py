from openalea.plantgl.gui.qt.QtCore import *
from openalea.plantgl.gui.qt.QtGui import *
from .theme_selector import Theme

class Module:

    def __init__(self, window):
        """
        :param window: The main window.
        """
        self.window = window
        self.viewer = self.window.viewer
        self.cursor = self.viewer.cursor
        self.isListening = False

    def listenEvents(self, enable=True):
        """
        Enable or disable event listening.
        :param enable: Enable or disable.
        :return: None
        """
        if enable == self.isListening:
            # No change made
            return

        if enable:
            self.viewer.registerEventListener(self)
        else:
            self.viewer.unregisterEventListener(self)

        self.isListening = enable

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

    def themeUpdateEvent(self, theme: Theme):
        pass

    def fastDraw(self):
        pass

    def draw(self):
        pass

    def postDraw(self):
        pass

    def drawWithNames(self):
        pass

    def endSelection(self, point: QPoint):
        pass

    def postSelection(self, point: QPoint):
        pass
