#! /usr/bin/env python3
class MateriaConTrabajos:
    def __init__(self, idm, nombre, ultima, cantidad, 
                 docente, sticky, logo, mail):
        self.id = idm
        self.nombre = nombre
        self.ultima = ultima
        self.cantidad = cantidad
        self.docente = docente
        self.sticky = sticky
        self.logo = logo
        self.mail = mail

    def cargar_trabajos(self, lista_de_trabajos):
        self.lt = lista_de_trabajos


