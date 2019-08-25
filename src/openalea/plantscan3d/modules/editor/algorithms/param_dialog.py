from openalea.plantgl.gui.qt.QtCore import *
from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.scenegraph import QuantisedFunction

# Parameters values cache
paramsCache = dict()

def getParamCache(name, defaultValue):
    """
    :param name: Name of the parameter set.
    :param defaultValue: The default values.
    :return: *
    """
    if name in paramsCache:
        return paramsCache[name]
    else:
        return defaultValue

def setParamCache(name, value):
    """
    Cache the parameter values.
    :param name: Name of the parameter set.
    :param value: The values to store.
    :return: None
    """
    paramsCache[name] = value

def create(parent, title, listparam):
    """
    Create a parameters dialog.
    :param parent: The parent widget.
    :param title: The title of the dialog.
    :param listparam: THe list of the parameters.
    :return: MDialog
    """
    class MDialog(QDialog):
        def __init__(self, parent):
            QDialog.__init__(self, parent)
            self.resultGetter = []

        def getParams(self):
            result = [box() for box in self.resultGetter]
            setParamCache(title, result)
            return result

    prevparam = getParamCache(title, None)
    if prevparam and len(prevparam) != len(listparam):
        prevparam = None

    Dialog = MDialog(parent)
    gridLayout = QGridLayout(Dialog)
    sectionLabel = QLabel(Dialog)
    sectionLabel.setText(title)
    gridLayout.addWidget(sectionLabel, 0, 0, 1, 2)
    space = QSpacerItem(1, 10)
    gridLayout.addItem(space, 1, 0, 1, 2)
    row = 2

    nbparam = 0
    for paraminfo in listparam:
        if len(paraminfo) == 3:
            pname, ptype, pdefvalue = paraminfo
            pparam = {}
        else:
            pname, ptype, pdefvalue, pparam = paraminfo
        if prevparam:
            pdefvalue = prevparam[nbparam]
        sectionLabel = QLabel(Dialog)
        sectionLabel.setText(pname)
        gridLayout.addWidget(sectionLabel, row, 0, 1, 1)
        if ptype == int:
            valuebox = QSpinBox(Dialog)
            if 'range' in pparam:
                valuebox.setRange(*pparam['range'])
            else:
                valuebox.setMinimum(-9999999999)
                valuebox.setMaximum(9999999999)
            valuebox.setValue(pdefvalue)
            gridLayout.addWidget(valuebox, row, 1, 1, 1)
            Dialog.resultGetter.append(valuebox.value)
        elif ptype == float:
            valuebox = QDoubleSpinBox(Dialog)
            if 'decimals' in pparam:
                valuebox.setDecimals(pparam['decimals'])
            else:
                valuebox.setDecimals(5)
            valuebox.setMinimum(-9999999999)
            valuebox.setMaximum(9999999999)
            valuebox.setValue(pdefvalue)
            gridLayout.addWidget(valuebox, row, 1, 1, 1)
            Dialog.resultGetter.append(valuebox.value)
        elif ptype == bool:
            valuebox = QCheckBox(Dialog)
            valuebox.setValue(pdefvalue)
            gridLayout.addWidget(valuebox, row, 1, 1, 1)
            Dialog.resultGetter.append(valuebox.isChecked)
        elif ptype == str:
            valuebox = QTextEdit(Dialog)
            gridLayout.addWidget(valuebox, row, 1, 1, 1)
            valuebox.setPlainText(pdefvalue)
            Dialog.resultGetter.append(valuebox.toPlainText)
        elif ptype == QuantisedFunction:
            from openalea.plantgl.gui.curve2deditor import Curve2DEditor, FuncConstraint
            valuebox = Curve2DEditor(Dialog)
            valuebox.pointsConstraints = FuncConstraint()
            if pdefvalue: valuebox.setCurve(pdefvalue)
            row += 1
            gridLayout.addWidget(valuebox, row, 0, 1, 2)
            Dialog.resultGetter.append(valuebox.getCurve)
        row += 1
        nbparam += 1

    buttonBox = QDialogButtonBox(Dialog)
    buttonBox.setOrientation(Qt.Horizontal)
    buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.accepted.connect(Dialog.accept)
    buttonBox.rejected.connect(Dialog.reject)
    gridLayout.addWidget(buttonBox, row, 1, 1, 1)

    return Dialog
