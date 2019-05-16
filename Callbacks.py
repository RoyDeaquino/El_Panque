class Callbacks:
    """Funciones que se utilizan en el frame de caja"""
    def __init__(self, parent):
        self.gui = parent

    def _quit(self):
        """Funcion de salida del frame"""
        self.gui.root.quit()
        self.gui.root.destroy()
        exit()


