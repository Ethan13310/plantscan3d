from OpenGL.GL import *
from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantscan3d.module import Module
from openalea.plantscan3d.slider_widget import SliderWidget

class ClippingPlane(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        self.enabled = False
        self.frontVisibility = 0
        self.backVisibility = 1

        self.dock, self.dockContainer = self.window.getDockWidget('Clipping Planes')
        self.window.setDockWidgetHeaderColor(self.dock, (230, 126, 34))
        self.__setupDockWidget(self.dockContainer)

    def draw(self):
        """
        Draw event.
        :return: None
        """
        if self.enabled:
            self.__apply()
        else:
            glDisable(GL_CLIP_PLANE0)
            glDisable(GL_CLIP_PLANE1)

    def __apply(self):
        """
        Apply the clipping plane.
        :return: None
        """
        glPushMatrix()
        glLoadIdentity()

        camera = self.viewer.camera()
        zNear = camera.zNear()
        zFar = camera.zFar()
        zDelta = zFar - zNear

        self.__applyFront(zNear, zDelta)
        self.__applyBack(zNear, zDelta)

        glPopMatrix()

    def __applyFront(self, zNear, zDelta):
        """
        Apply the front clipping plane.
        :return: None
        """
        if self.frontVisibility > 0.0:
            eq = [0.0, 0.0, -1.0, -(zNear + zDelta * self.frontVisibility)]
            glClipPlane(GL_CLIP_PLANE0, eq)
            glEnable(GL_CLIP_PLANE0)
        else:
            glDisable(GL_CLIP_PLANE0)

    def __applyBack(self, zNear, zDelta):
        """
        Apply the back clipping plane.
        :return: None
        """
        if self.backVisibility < 1.0:
            eq = [0.0, 0.0, 1.0, zNear + zDelta * self.backVisibility]
            glClipPlane(GL_CLIP_PLANE1, eq)
            glEnable(GL_CLIP_PLANE1)
        else:
            glDisable(GL_CLIP_PLANE1)

    def __setupDockWidget(self, container: QWidget):
        """
        Setup the dock widget interface.
        :param container: The container Widget.
        :return: None
        """
        layout = QVBoxLayout(container)

        # Checkbox enable/disable
        self.visibilityEnabled = QCheckBox(container)
        self.visibilityEnabled.setChecked(False)
        self.visibilityEnabled.setText('Enabled')

        # Near clipping plane
        self.frontVisibilitySlider = SliderWidget(container)
        self.frontVisibilitySlider.setEnabled(False)
        self.frontVisibilitySlider.setup('Near', 0, 1, 0, 3)

        # Far clipping plane
        self.backVisibilitySlider = SliderWidget(container)
        self.backVisibilitySlider.setEnabled(False)
        self.backVisibilitySlider.setup('Far', 0, 1, 1, 3)

        layout.addWidget(self.visibilityEnabled)
        layout.addWidget(self.frontVisibilitySlider)
        layout.addWidget(self.backVisibilitySlider)

        # Main spacer
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Events
        self.visibilityEnabled.stateChanged.connect(self.__onEnableClippingPlanes)
        self.frontVisibilitySlider.valueFloatChanged.connect(self.__onFrontVisibilityChanged)
        self.backVisibilitySlider.valueFloatChanged.connect(self.__onBackVisibilityChanged)

    def __onEnableClippingPlanes(self, enabled: bool):
        """
        Enable or disable clipping planes event.
        :param enabled: Are clipping planes enabled?
        :return: None
        """
        self.frontVisibilitySlider.setEnabled(enabled)
        self.backVisibilitySlider.setEnabled(enabled)
        self.enabled = enabled
        self.viewer.updateGL()

    def __onFrontVisibilityChanged(self, value: float):
        """
        Change front visibility distance event.
        :param value: The new font visiblity distance.
        :return: None
        """
        self.frontVisibility = value
        self.viewer.updateGL()

    def __onBackVisibilityChanged(self, value: float):
        """
       Change back visibility distance event.
       :param value: The new back visiblity distance.
       :return: None
       """
        self.backVisibility = value
        self.viewer.updateGL()

# Module export
export = ClippingPlane
