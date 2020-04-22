#! /usr/bin/env python3
class Curso:
    def __init__(self, id, anio, division, descripcion):
        self.id = id
        self.anio = anio
        self.division = division
        self.descripcion = descripcion

    def __str__(self):
        return self.descripcion

