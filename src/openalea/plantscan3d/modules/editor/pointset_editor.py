from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.gui.editablectrlpoint import *
from openalea.plantscan3d.slider_widget import SliderWidget
from openalea.plantscan3d.backup import BackupObject
from openalea.plantscan3d.module import Module
import PyQGLViewer

class PointsInfos:

    def __init__(self):
        self.pointWidth = 2
        self.selectedPoints = Index([])

class PointsetEditor(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        self.points = None
        self.pointsRep = None
        self.pointsInfos = PointsInfos()
        self.pointsAttributeRep = None
        self.translation = None
        self.shapeSelection = None
        self.shapePoints = None
        self.selectBufferSizeValue = 0

        # Menu
        self.window.menu.addSeparator('Points')
        self.actionRemoveSelection = self.window.menu.addAction('Points', 'Remove Selection')
        self.actionKeepSelection = self.window.menu.addAction('Points', 'Keep Selection')
        self.actionDeselect = self.window.menu.addAction('Points', 'Deselect')

        self.actionRemoveSelection.triggered.connect(self.deleteSelection)
        self.actionKeepSelection.triggered.connect(self.keepSelection)
        self.actionDeselect.triggered.connect(self.deselectPoints)

        self.actionRemoveSelection.setShortcut(QKeySequence('Del'))
        self.actionKeepSelection.setShortcut(QKeySequence('Shift+Del'))
        self.actionDeselect.setShortcut(QKeySequence('Ctrl+D'))

        # Dock Widget
        self.dock, self.dockContainer = self.window.getDockWidget('Display')
        self.window.setDockWidgetHeaderColor(self.dock, (231, 76, 60))
        self.__setupDockWidget(self.dockContainer)

        # Backup
        self.viewer.backup.declare_backup('points', [
            BackupObject('points', self,
                getmethod=lambda o, n: {
                    'pointList': getattr(o, n).pointList,
                    'colorList': getattr(o, n).colorList
                },
                setmethod=lambda o, n, no: setattr(o, n, PointSet(no['pointList'], no['colorList'])),
                copymethod=lambda o: {
                    'pointList': Point3Array(o.pointList),
                    'colorList': Color4Array(o.colorList)
                }
            ),
            BackupObject('pointsInfos', self),
        ],
        lambda: self.setPoints(self.points))

    def fastDraw(self):
        """
        Fast draw event.
        :return: None
        """
        if self.points:
            self.pointsRep.apply(self.viewer.glRenderer)

    def draw(self):
        """
        Draw event.
        :return: None
        """
        if self.points:
            self.pointsRep.apply(self.viewer.glRenderer)

    def setNewPointset(self, pointSet):
        """
        Set a new point set.
        :param pointSet: The new point set.
        :return: None
        """
        self.pointsInfos.selectedPoints = Index([])
        self.setPoints(pointSet)
        self.viewer.updateGL()

    def selectPoints(self, points):
        """
        Create a new selection.
        :param points: Points to select.
        :return: None
        """
        if self.points is not None:
            self.pointsInfos.selectedPoints = points
            self.createPointsRepresentation()
            self.viewer.updateGL()

    def deselectPoints(self):
        """
        Deselect all points.
        :return: None
        """
        self.selectPoints(Index([]))

    def deleteSelection(self):
        """
        Delete all selected points.
        :return: None
        """
        if self.points is None or len(self.pointsInfos.selectedPoints) == 0:
            # No point selected
            return

        self.viewer.createBackup('points')

        self.setNewPointset(PointSet(
            self.points.pointList.opposite_subset(self.pointsInfos.selectedPoints),
            self.points.colorList.opposite_subset(self.pointsInfos.selectedPoints)
        ))

    def keepSelection(self):
        """
        Delete non-selected points.
        :return: None
        """
        if len(self.pointsInfos.selectedPoints) == 0:
            # No point selected
            return

        self.viewer.createBackup('points')

        self.setNewPointset(PointSet(
            self.points.pointList.subset(self.pointsInfos.selectedPoints),
            self.points.colorList.subset(self.pointsInfos.selectedPoints)
        ))

    def setPoints(self, points, keepInfos: bool=False):
        self.points = points
        self.pointsAttributeRep = None

        if self.pointSizeSlider is not None:
            self.pointSizeSlider.setEnabled(True)

        if not keepInfos:
            self.pointsInfos = PointsInfos()

        if self.points.colorList is None:
            self.points.colorList = generate_point_color(self.points)

        self.selectBufferSizeValue = len(self.points.pointList) * 5
        self.viewer.setSelectBufferSize(self.selectBufferSizeValue)

        self.adjustTo(points)
        self.createPointsRepresentation()

    def adjustTo(self, obj):
        boundingBox = BoundingBox(obj)
        toVector = lambda v: PyQGLViewer.Vec(v.x, v.y, v.z)

        lowerLeft = toVector(boundingBox.lowerLeftCorner)
        upperRight = toVector(boundingBox.upperRightCorner)

        self.viewer.setSceneBoundingBox(lowerLeft, upperRight)

    def createPointsRepresentation(self):
        pointList = self.points.pointList
        colorList = self.points.colorList

        if len(self.pointsInfos.selectedPoints) > 0:
            selectedPoints, otherPoints = pointList.split_subset(self.pointsInfos.selectedPoints)
            selectedColors, otherColors = colorList.split_subset(self.pointsInfos.selectedPoints)

            selectedColors = Color4Array([Color4(255, 0, 0, 0) for i in range(len(selectedColors))])

            self.shapePoints = Shape(PointSet(otherPoints, otherColors, width=self.pointsInfos.pointWidth), self.viewer.pointMaterial)
            self.shapeSelection = Shape(PointSet(selectedPoints, selectedColors, width=self.pointsInfos.pointWidth + 2), self.viewer.pointMaterial)
            self.pointsRep = Scene([self.shapePoints, self.shapeSelection])
        else:
            self.shapePoints = Shape(PointSet(pointList, colorList, width=self.pointsInfos.pointWidth), self.viewer.pointMaterial)
            self.pointsRep = Scene([self.shapePoints])

        if self.pointSizeSlider is not None:
            self.pointSizeSlider.setValue(self.pointsInfos.pointWidth)

    def checkPointsLoaded(self) -> bool:
        """
        Check whether the points are loaded.
        Display a warning message box if they're not.
        :return: bool
        """
        if self.points is not None:
            # Loaded
            return True

        # Not loaded
        QMessageBox.warning(self.window, 'PlantScan3D', 'No points loaded.')
        return False

    def setPointWidth(self, value: int):
        self.pointsInfos.pointWidth = value
        if self.pointsRep:
            self.pointsRep[0].geometry.width = value
            if len(self.pointsInfos.selectedPoints) > 0:
                self.pointsRep[1].geometry.width = value + 2
            self.viewer.updateGL()

    def __setupDockWidget(self, container: QWidget):
        """
        Setup the dock widget interface.
        :param container: The container Widget.
        :return: None
        """
        layout = QVBoxLayout(container)

        # Near clipping plane
        self.pointSizeSlider = SliderWidget(container)
        self.pointSizeSlider.setup('Point Width', 1, 10, 2)
        self.pointSizeSlider.setEnabled(False)

        layout.addWidget(self.pointSizeSlider)

        # Main spacer
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Events
        self.pointSizeSlider.valueChanged.connect(self.setPointWidth)

# Module export
export = PointsetEditor
