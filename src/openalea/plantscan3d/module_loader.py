import importlib.util
import sys
import os

class ModuleLoader:

    def __init__(self, configFile: str):
        """
        :param configFile: Modules configuration file.
        """
        self.configFile = configFile
        self.modules = []
        self.moduleNames = {}

    def load(self, window) -> list:
        """
        Load all modules.
        :param window: The main window.
        :return: list
        """
        self.modules = []
        paths, modules = self.__getLoadInfos()

        for moduleName in modules:
            name = self.__getModuleName(moduleName)
            try:
                module = self.__loadModule(moduleName, paths)
                module = module.export

                if module is None:
                    # The module has no 'export' variable
                    raise ImportError()

                module = module(window)
            except Exception as e:
                print('Could not load module:', name)
                print('Reason:', str(e))
            else:
                self.modules.append(module)
                self.moduleNames[name] = module
                print('Loaded module:', name)

        return self.modules

    def get(self, name: str):
        """
        Get a module by its name.
        :param name: The name of the module
        :return: object
        """
        return self.moduleNames[name] if name in self.moduleNames else None

    def __getLoadInfos(self) -> tuple:
        """
        Get the module load infos, by reading the configuration file.
        :return: tuple
        """
        paths = []
        modules = []
        type = None
        file = open(self.configFile, 'r')

        for config in file:
            config = config.rstrip('\n')

            if len(config) == 0:
                # Empty line
                pass
            elif config == '[path]':
                # Path section
                type = 'path'
            elif config == '[modules]':
                # Module section
                type = 'modules'
            else:
                # Values
                if type == 'path':
                    paths.append(config)
                else:
                    modules.append(config)

        return paths, modules

    def __loadModule(self, moduleName: str, paths: list):
        """
        Load a module.
        :param moduleName: Name of the module.
        :param paths: Possible paths to the module file.
        :return: object
        """
        for path in paths:
            fullPath = self.__getModuleFullPath(moduleName, path)
            try:
                # We try to load the module
                if fullPath is None:
                    module = importlib.import_module(path + '.' + moduleName)
                else:
                    spec = importlib.util.spec_from_file_location(moduleName, fullPath)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[spec.name] = module
                    spec.loader.exec_module(module)
            except:
                pass
            else:
                return module

        # The module could not be found within the given paths
        raise ImportError('Module not found')

    def __getModuleFullPath(self, moduleName: str, path: str):
        """
        Get the full path to a module. Return None if the module path is
        a package name.
        :param moduleName: The name of the module.
        :param path: THe path to the module
        :return: str
        """
        if '/' in path and '/' in moduleName:
            # Full path
            return os.path.join(path, moduleName)
        else:
            # Package name
            return None

    def __getModuleName(self, moduleName: str) -> str:
        """
        Extract the module name.
        :param moduleName: The full module name
        :return: str
        """
        moduleName = moduleName.split('/')[-1]
        moduleName = moduleName.split('.')

        if moduleName[-1].lower() == 'py':
            # We remove the file extension
            if len(moduleName) >= 2:
                return moduleName[-2]
            else:
                # Invalid name
                return str()
        else:
            return moduleName[-1]
