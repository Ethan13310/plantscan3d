from openalea.plantgl.gui.editablectrlpoint import *
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

        # Dock Widget
        self.dock, self.dockContainer = self.window.getDockWidget('Display')
        self.window.setDockWidgetHeaderColor(self.dock, (231, 76, 60))

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
        if len(self.pointsInfos.selectedPoints) == 0:
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

# Module export
export = PointsetEditor
