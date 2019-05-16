# -*- coding: utf-8 -*-
from message import MessagePopup


class I18N:
    """Internationalization"""
    def __init__(self, language):
        if language == 'en':
            self.languageEnglish()
        elif language == 'es':
            self.languageSpanish()
        else:
            msg = MessagePopup('Unsupported language', 'The language selected is not supported', 'w')
            msg()

    def languageEnglish(self):
        self.title = "El panque"
        self.tab1Text = "Cash Register"

        self.pedidos = "Orders"
        self.new = "New"
        self.list = "List"
        self.search = "Search"
        self.exit = "Exit"

        self.store = "Store"
        self.new_product = "New Product"

        self.inv = "Stocktaking"

        self.help = "Help"
        self.lang = "Language"
        self.about = "About"

        self.caja = "Cash register"
        self.total = "Total"
        self.cash = "Cash"
        self.change = "Change"

        self.es = "Español"
        self.en = "Ingles"

        self.product = "Product"
        self.amount = "Amount"
        self.cost = "Cost"

        self.products = "Products"
        self.stock = "Stock"
        self.edit = "Edit"
        self.details = "Details"
        self.info = "Information"

        self.toplevel_title = "Enter the code"

        self.name = "Name"
        self.sizes = "Size"
        self.save = "Save"

        self.close = "Close"

        self.msgStockTitle = "Invalid stock quantity"
        self.msgStockBody = "Verify that you are entering a number from 1 to 100"

        self.msgCostTitle = "Invalid product cost"
        self.msgCostBody = "Verify that you are entering a number between 1 and 10000"



    def languageSpanish(self):
        self.title = "El panque"
        self.tab1Text = "Caja"

        self.pedidos = "Pedidos"
        self.new = "Nuevo"
        self.list = "Listado"
        self.search = "Buscar"
        self.exit = "Salir"

        self.store = "Almacén"
        self.new_product = "Nuevo Producto"

        self.inv = "Inventario"

        self.help = "Ayuda"
        self.lang = "Idioma"
        self.about = "Acerca de"

        self.caja = "Caja"
        self.total = "Total"
        self.cash = "Efectivo"
        self.change = "Cambio"

        self.es = "Spanish"
        self.en = "English"

        self.product = "Producto"
        self.amount = "Cantidad"
        self.cost = "Costo"

        self.products = "Productos"
        self.stock = "Existencias"
        self.edit = "Editar"
        self.details = "Detalles"
        self.info = "Información"

        self.toplevel_title = "Ingrese el código"

        self.name = "Nombre"
        self.sizes = "Tamaño"
        self.save = "Guardar"

        self.close = "Cerrar"

        self.msgStockTitle = "Cantidad de existencias inválido"
        self.msgStockBody = "Verifique que este ingresando un número del 1 al 100"

        self.msgCostTitle = "Costo del producto inválido"
        self.msgCostBody = "Verifique que este ingresando un número entre el 1 y el 10000"


if __name__ == '__main__':
    app = I18N('ep')
    app()
    app.mainloop()
