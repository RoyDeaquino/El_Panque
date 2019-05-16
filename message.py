from tkinter import messagebox as msg
from tkinter import Tk


class MessagePopup:
    """MesageBox popup personalizado"""
    def __init__(self, title, message, flag):
        """Ejecuta la funcion en base al tipo de mensaje requerido en la variable flag"""
        root = Tk()
        root.withdraw()
        if flag == 'w':
            self.popupWarning(title, message)
        elif flag == 'e':
            self.popuperror(title, message)
        elif flag == 'i':
            self.popupInfo(title, message)
        else:
            self.popupWarning(title, message)

    def popuperror(self, title, message):
        """Lanza un error de tipo showerror"""
        msg.showerror(title, message)

    def popupWarning(self, title, message):
        """Lanza un mensage de tipo showwarning"""
        msg.showwarning(title, message)

    def popupInfo(self, title, message):
        """Lanza un mensaje de tipo showinfo"""
        msg.showinfo(title, message)


if __name__ == '__main__':
    app = MessagePopup('Title', 'Test', 'e')
    app.mainLoop()
