#! /usr/bin/env python3
class Materia:
    def __init__(self, id, nombre, curso, logo = 'pizarra.png', 
            sticky = False, docente = None, mail= None):
        self.id = id
        self.nombre = nombre
        self.curso = curso
        self.logo = logo
        self.sticky = sticky
        self.docente = docente
        self.mail = mail

    def __str__(self):
        return f"{self.nombre} ({self.curso.descripcion})"

   

