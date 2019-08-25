from openalea.plantscan3d.module import Module

class MTGEditor(Module):

    def __init__(self, window):
        """
        :param window: The main window.
        """
        Module.__init__(self, window)

# Export module
export = MTGEditor
