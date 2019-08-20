try:
    # We check the release type
    import openalea.plantscan3d.py2exe_release
    py2ExeRelease = True
    print('Py2Exe Release')

except ImportError:
    # Not a Py2Exe release
    py2ExeRelease = False
    print('Std Release')

def isPy2ExeRelease() -> bool:
    """
    Check whether this release is a Py2Exe release.
    :return: bool
    """
    return py2ExeRelease

def isStdRelease() -> bool:
    """
    Check whether this release is a standard release.
    :return: bool
    """
    return not py2ExeRelease

if isStdRelease():
    from . import ui_compiler
    import inspect
    import os

def compileUi(relativePath: str):
    """
    Compile a Qt UI file.
    :param relativePath: The relative path to the UI file.
    :return: None
    """
    if isStdRelease():
        path = os.path.dirname((inspect.stack()[1])[1])
        ui_compiler.check_ui_generation(os.path.join(path, relativePath))

def compileRc(relativePath: str):
    """
    Compile a Qt Resource file.
    :param relativePath: The relative path to the Resource file.
    :return: None
    """
    if isStdRelease():
        path = os.path.dirname((inspect.stack()[1])[1])
        ui_compiler.check_rc_generation(os.path.join(path, relativePath))
