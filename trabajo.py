#! /usr/bin/env python3
import datetime

class Trabajo:
    def __init__(self, id, titulo, descripcion, publicado, entrega, archivo, 
            materia, es_url = False):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.archivo = archivo
        self.es_url = es_url
        self.materia = materia
        publicado = publicado.split("-")
        self.publicado = datetime.date(int(publicado[0]),int(publicado[1]),int(publicado[2]))
        if entrega:
            entrega = entrega.split("-")
            self.entrega = datetime.date(int(entrega[0]),int(entrega[1]),int(entrega[2]))
        else:
            self.entrega = None






