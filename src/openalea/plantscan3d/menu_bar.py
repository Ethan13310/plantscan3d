from openalea.plantgl.gui.qt.QtGui import *

class MenuBar:

    def __init__(self, window):
        """
        :param window: The main window.
        """
        self.window = window
        self.menuBar: QMenuBar = window.menuBar

        self.fileHasSeparator = False
        self.editHasSeparator = False
        self.viewHasSeparator = False

        # Menu list
        self.menus = {
            'File': self.window.menuFile,
            'Edit': self.window.menuEdit,
            'View': self.window.menuView
        }

    def addExportAction(self, text: str) -> QAction:
        """
        Add a new action to the 'Export' menu.
        :param text: The text of the action.
        :return: QAction
        """
        menu = self.window.menuExportView
        action = QAction(text, menu)
        menu.insertAction(self.window.actionSaveSnapshot, action)
        return action

    def addMenu(self, mainMenu: str, menuTitle: str) -> QMenu:
        """
        Add a new sub-menu to the specified main menu.
        :param mainMenu: The title of the main menu.
        :param menuTitle: The title of the sub-menu to add.
        :return: QMenu
        """
        mainMenuTitle = mainMenu.title()
        mainMenu = self.__getMainMenu(mainMenuTitle)

        subMenu = QMenu(menuTitle, mainMenu)
        self.__insert(mainMenu, mainMenuTitle, subMenu)
        return subMenu

    def addAction(self, mainMenu: str, actionText: str) -> QAction:
        """
        Add a new action to the specified main menu.
        :param mainMenu: The title of the main menu.
        :param actionText: The title of the action to add.
        :return: QMenu
        """
        mainMenuTitle = mainMenu.title()
        mainMenu = self.__getMainMenu(mainMenuTitle)

        action = QAction(actionText, mainMenu)
        self.__insert(mainMenu, mainMenuTitle, action)
        return action

    def addSeparator(self, menuTitle: str):
        """
        Add a separator at the end of the menu, if necessary.
        :param menuTitle: The title of the menu.
        :return: None
        """
        title = menuTitle.title()

        if title in self.menus:
            # The menu exists, we add a separator at its end
            menu = self.menus[title]
            separator = QAction(menu)
            separator.setSeparator(True)
            self.__insert(menu, title, separator)

    def __getMainMenu(self, title: str) -> QMenu:
        """
        Add a new main menu if it does not exist yet.
        :param title: The title of the menu.
        :return: QMenu
        """
        title = title.title()

        if title in self.menus:
            # The main menu already exists
            return self.menus[title]

        # Otherwise, we create it
        menu = self.menuBar.addMenu(title)
        self.menus[title] = menu
        return menu

    def __insert(self, mainMenu, mainMenuTitle, action):
        """
        Insert an action into a menu.
        :param mainMenu: The QMenu where to insert the action.
        :param mainMenuTitle: The title of the QMenu.
        :param action: The action to insert.
        :return: None
        """
        if mainMenuTitle == 'File':
            # Menu 'File'
            mainMenu.insertAction(self.window.actionExportViewBefore, action)
            if not self.fileHasSeparator:
                mainMenu.insertSeparator(self.window.menuExportView.menuAction())
                self.fileHasSeparator = True

        elif mainMenuTitle == 'Edit':
            # Menu 'Edit'
            if not self.editHasSeparator:
                mainMenu.addSeparator()
                self.editHasSeparator = True
            mainMenu.addAction(action)

        elif mainMenuTitle == 'View':
            # Menu 'View'
            mainMenu.insertAction(self.window.actionThemeBefore, action)
            if not self.viewHasSeparator:
                mainMenu.insertSeparator(self.window.menuTheme.menuAction())
                self.viewHasSeparator = True

        else:
            # Other menus
            mainMenu.addAction(action)
