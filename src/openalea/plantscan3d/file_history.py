from collections import OrderedDict

class FileHistory:
    def __init__(self, menu = None, callfunc = None, maxsize = 20):
        self.setMenu(menu)
        self.callfunc = callfunc
        self.maxsize = maxsize
        self.menu = None
        self.files = OrderedDict([])
        self.__discardedmenu = False
        self.clear()

    def setMenu(self, menu):
        self.menu = menu
        if self.menu: 
            self.menu.aboutToShow.connect(self.updateMenu)

    def add(self, file, param = None):
        self.files[file] = param
        while len(self.files) >= self.maxsize:
            del self.files[list(self.files.keys())[-1]]
        self.__discardedmenu = True

    def remove(self, file):
        del self.files[file]
        self.__discardedmenu = True

    def clear(self):
        self.files = OrderedDict([])
        self.__discardedmenu = True

    def check(self):
        import os
        files = OrderedDict([])
        for file, ftype in list(self.files.items()):
            if os.path.exists(file):
                files[file] = ftype

        if len(files) != len(self.files):
            self.files = files
            self.__discardedmenu = True

    def getLastFile(self, ftype = None):
        for fname, data in reversed(list(self.files.items())):
            if data == ftype: return fname

    def updateMenu(self):
        from os.path import basename 
        if self.__discardedmenu:
            self.__discardedmenu = False
            self.menu.clear()
            def callbackgenerator(fname, param = None):
                if param:
                    def callback():
                        return self.callfunc(fname, param)
                else:
                    def callback():
                        return self.callfunc(fname)
                return callback
            i = 0
            for fname, param in list(self.files.items()):
                i += 1
                self.menu.addAction(str(i) + '. ' + basename(fname), callbackgenerator(fname, param))
            if i == 0:
                action = self.menu.addAction('No Recent File')
                action.setEnabled(False)
            else:
                self.menu.addSeparator()
                self.menu.addAction('Clear History', self.clear)

    def retrieveSettings(self, settings):
        settings.beginGroup("FileHistory")
        files = settings.value("RecentFiles")
        settings.endGroup()

        if not files is None:
            files = [file.split(':',1) for file in files]
            files = OrderedDict([(str(fname),str(ftype)) for ftype,fname in files])
            self.files = files
            self.check()

    def setSettings(self, settings):
        settings.beginGroup("FileHistory")
        files = [ftype+':'+fname for fname, ftype in list(self.files.items())]
        settings.setValue("RecentFiles",files)
        settings.endGroup()