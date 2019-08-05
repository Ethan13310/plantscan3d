from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.gui.editablectrlpoint import Material

class Theme:

    def __init__(self, name: str):
        """
        :param name: The name of the theme.
        """
        self.name = name
        self.background = None
        self.points = None
        self.contractedPoints = None
        self.ctrlPoints = None
        self.newCtrlPoints = None
        self.selectedCtrlPoints = None
        self.edgeInf = None
        self.edgePlus = None
        self.radius = None
        self.direction = None
        self.model3d = None
        self.hull3d = None
        self.localAttractors = None
        self.cone = None
        self.taggedCtrlPoint = None
        self.untaggedCtrlPoint = None
        self.upscaleCtrlPoint = None

    def __getitem__(self, key: str):
        """
        Get the specified value.
        :param key: The key.
        :return: *
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value):
        """
        Set the specified value.
        :param key: The key.
        :param value: The value.
        :return: None
        """
        if hasattr(self, key):
            setattr(self, key, value)

    def getName(self) -> str:
        """
        Get the name of the theme.
        :return: str
        """
        return self.name

# Theme List
ThemeList = {
    'Black': {
        'background': (0, 0, 0),
        'points': (180, 180, 180),
        'contractedPoints': (255, 0, 0),
        'ctrlPoints': (250,250,250),
        'newCtrlPoints': (30, 250, 250),
        'selectedCtrlPoints': (30, 250, 30),
        'edgeInf': (255, 255, 255),
        'edgePlus': (255, 0, 0),
        'radius': (200, 200, 200),
        'direction': (255, 255, 255),
        'model3d': (128, 64, 0),
        'hull3d': (0, 200, 0),
        'localAttractors': (255, 255, 0),
        'cone': (255, 255, 0),
        'taggedCtrlPoint': (255, 0, 0),
        'untaggedCtrlPoint': (255, 255, 255),
        'upscaleCtrlPoint': [(0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    },
    'White': {
        'background': (255, 255, 255),
        'points': (180, 180, 180),
        'contractedPoints': (255, 0, 0),
        'ctrlPoints': (250, 30, 30),
        'newCtrlPoints': (30, 250, 250),
        'selectedCtrlPoints': (30, 250, 30),
        'edgeInf': (0, 0, 0),
        'edgePlus': (200, 200, 0),
        'radius': (100, 100, 100),
        'direction': (0, 0, 0),
        'model3d': (128, 64, 0),
        'hull3d': (0, 200, 0),
        'localAttractors': (255, 255, 0),
        'cone': (255, 255, 0),
        'taggedCtrlPoint': (255, 0, 0),
        'untaggedCtrlPoint': (0, 0, 0),
        'upscaleCtrlPoint': [(0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    }
}

class ThemeSelector:

    def __init__(self, widget):
        """
        :param widget: The QWidget.
        """
        # Default theme is empty
        self.theme = Theme('Default')
        self.widget = widget

    def __getitem__(self, key: str):
        """
        Get the specified value of the current theme.
        :param key: The key.
        :return: *
        """
        return self.theme[key]

    def __setitem__(self, key, value):
        """
        Set the specified value of the current theme.
        :param key: The key.
        :param value: The value.
        :return: None
        """
        self.theme[key] = value

    def get(self) -> Theme:
        """
        Get the current theme.
        :return: Theme
        """
        return self.theme

    def set(self, theme):
        """
        Set the current theme.
        :param theme: The name of the theme, or the theme itself.
        :return: None
        """
        if isinstance(theme, Theme):
            self.theme = theme
        elif theme in ThemeList:
            # Set by name
            self.theme = Theme(theme)

            for key in ThemeList[theme]:
                self.theme[key] = ThemeList[theme][key]
        else:
            raise ValueError('Invalid Theme')

        self.updateWidget()

    def getName(self) -> str:
        """
        Get the name of the current theme.
        :return: str
        """
        return self.theme.getName()

    def restore(self, settings):
        """
        Retore the theme from the settings.
        :param settings: The settings.
        :return: None
        """
        default = 'Black'
        settings.beginGroup('Theme')
        name = settings.value('Name', default)
        settings.endGroup()

        try:
            self.set(name)
        except:
            self.set(default)

    def save(self, settings):
        """
        Save the theme to the settings.
        :param settings: The settings.
        :return: None
        """
        settings.beginGroup('Theme')
        settings.setValue('Name', self.getName())
        settings.endGroup()

    def updateWidget(self):
        """
        Update widget data.
        :return: None
        """
        # Widget background color
        self.widget.setBackgroundColor(QColor(*self.theme.background))

        # Materials
        self.widget.pointMaterial = Material(self.theme.points, 1)
        self.widget.contractedpointMaterial = Material(self.theme.contractedPoints, 1)
        self.widget.ctrlPointColor = self.theme.ctrlPoints
        self.widget.newCtrlPointColor = self.theme.newCtrlPoints
        self.widget.edgeInfMaterial = Material(self.theme.edgeInf, 1)
        self.widget.edgePlusMaterial = Material(self.theme.edgePlus, 1)
        self.widget.selectedPointColor = Material(self.theme.selectedCtrlPoints, 1)
        self.widget.radiusMaterial = Material(self.theme.radius, 1)
        self.widget.modelMaterial = Material(self.theme.model3d, 1, transparency=0.2)
        self.widget.hullMaterial = Material(self.theme.hull3d, 1, transparency=0.2)
