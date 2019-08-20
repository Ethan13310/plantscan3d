from OpenGL.GL import *
from openalea.plantgl.gui.qt.QtCore import *
from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.gui.editablectrlpoint import *
from openalea.plantscan3d.module import Module

class PointsetSelector(Module):

    # Selection modes
    AddSelect = 1
    HybridSelect = 2

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

        self.selectMode = None
        self.selectRect = None
        self.editor = self.getModule('pointset_editor', True)

    def mousePressEvent(self, event: QMouseEvent):
        """
        Mouse press event.
        :param event:
        :return: bool
        """
        if event.button() != Qt.LeftButton:
            return False

        if event.modifiers() == Qt.ShiftModifier:
            # Hybrid selection
            self.selectMode = self.HybridSelect
        elif event.modifiers() == (Qt.ShiftModifier | Qt.ControlModifier):
            # Add selection
            self.selectMode = self.AddSelect
        else:
            return False

        # Selection started
        self.selectRect = QRect(event.pos(), event.pos())
        return True

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Mouse release event.
        :param event:
        :return: bool
        """
        if self.selectMode is None:
            return False

        self.selectRect = self.selectRect.normalized()
        # Define selection window dimensions
        self.viewer.setSelectRegionWidth(self.selectRect.width())
        self.viewer.setSelectRegionHeight(self.selectRect.height())
        # Compute rectangle center and perform selection

        if self.editor.selectBufferSizeValue != self.viewer.selectBufferSize():
            self.viewer.setSelectBufferSize(self.editor.selectBufferSizeValue)
        self.viewer.select(self.selectRect.center())
        self.selectMode = None
        self.selectRect = None
        # Update display to show new selected objects
        self.editor.createPointsRepresentation()
        self.viewer.glRenderer.renderingMode = self.viewer.glRenderer.Dynamic
        self.viewer.updateGL()
        return False

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Mouse move event.
        :param event:
        :return: bool
        """
        if self.selectMode is not None:
            # We update the selection rectangle
            self.selectRect.setBottomRight(event.pos())
            self.viewer.updateGL()
            return True
        else:
            return False

    def postDraw(self):
        """
        Post draw event.
        :return: None
        """
        if self.selectRect is not None:
            self.__drawSelectionRectangle()

    def drawWithNames(self):
        """
        Draw with names event.
        :return: None
        """
        self.viewer.glRenderer.renderingMode = self.viewer.glRenderer.Selection
        self.viewer.glRenderer.selectionMode = self.viewer.glRenderer.SceneObjectNPrimitive

        if self.selectMode == self.AddSelect:
            # Additive selection
            Scene([Shape(PointSet(self.editor.points.pointList, self.editor.points.colorList), self.viewer.pointMaterial)]).apply(self.viewer.glRenderer)
        else:
            # Hybrid selection
            print('hybrid',len(self.editor.pointsRep[0].geometry.pointList))
            self.editor.pointsRep.apply(self.viewer.glRenderer)

    def endSelection(self, point: QPoint):
        """
        End selection event.
        :param point:
        :return: None
        """
        selection = self.viewer.getMultipleSelection()
        selectIndex = Index([])
        selectAlreadySelectedPoint = False

        if selection is not None:
            for zmin, zmax, id in selection:
                if self.selectMode == self.AddSelect or id[0] == self.editor.shapePoints.id:
                    selectIndex.append(id[1])
                elif len(self.editor.pointsInfos.selectedPoints) > 0 and id[0] == self.editor.shapeSelection.id:
                    if self.selectMode == self.HybridSelect:
                        selectAlreadySelectedPoint = True
                        break

            if selectAlreadySelectedPoint:
                selectIndex = Index([])
                for zmin, zmax, id in selection:
                    if id[0] == self.editor.shapeSelection.id:
                        selectIndex.append(id[1])
                self.editor.pointsInfos.selectedPoints = self.editor.pointsInfos.selectedPoints.opposite_subset(selectIndex)

        if not selectAlreadySelectedPoint:
            if self.selectMode == self.AddSelect:
                self.editor.pointsInfos.selectedPoints.append(selectIndex)
            else:
                self.editor.pointsInfos.selectedPoints = Index([])
                self.selectMode = self.AddSelect
                self.viewer.select(self.selectRect.center())

    def __drawSelectionRectangle(self):
        """
        Draw the selection rectangle.
        :return: None
        """
        self.viewer.startScreenCoordinatesSystem()
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)

        # Rectangle
        glColor4f(0.0, 0.0, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex2i(self.selectRect.left(), self.selectRect.top())
        glVertex2i(self.selectRect.right(), self.selectRect.top())
        glVertex2i(self.selectRect.right(), self.selectRect.bottom())
        glVertex2i(self.selectRect.left(), self.selectRect.bottom())
        glEnd()

        # Outline
        glLineWidth(2.0)
        glColor4f(0.4, 0.4, 0.5, 0.5)
        glBegin(GL_LINE_LOOP)
        glVertex2i(self.selectRect.left(), self.selectRect.top())
        glVertex2i(self.selectRect.right(), self.selectRect.top())
        glVertex2i(self.selectRect.right(), self.selectRect.bottom())
        glVertex2i(self.selectRect.left(), self.selectRect.bottom())
        glEnd()

        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        self.viewer.stopScreenCoordinatesSystem()

# Export module
export = PointsetSelector
