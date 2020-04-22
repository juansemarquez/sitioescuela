#! /usr/bin/env python3
import sqlite3
from repositorio_materia import RepositorioMateria
from materia import Materia
from curso import Curso
from trabajo import Trabajo

class RepositorioTrabajo:
    def __init__(self):
        self.bd = sqlite3.connect("bd.sqlite")
        self.bd.row_factory = sqlite3.Row
        self.cursor = self.bd.cursor()

    def get_all(self):
        rm = RepositorioMateria()
        trabajos_sql = "SELECT id, titulo, descripcion, fecha_publicada, \
            fecha_entrega, archivo, id_materia, es_url FROM material \
            order by id_materia, fecha_publicada;"
        self.cursor.execute(trabajos_sql)
        
        trabajos = []
        for f in self.cursor.fetchall():
            materia = rm.get_one(f[6])
            trabajos.append(Trabajo(f[0], f[1],f[2],f[3], f[4], f[5], materia, 
                                    f[7]))

        return trabajos

    def get_all_materia(self, materia):
        # Si me pasan un id_materia
        rm = RepositorioMateria()
        if type(materia) is not Materia:
            materia = rm.get_one(int(materia))
        
        trabajos_sql = "SELECT id, titulo, descripcion, fecha_publicada, \
            fecha_entrega, archivo, id_materia, es_url FROM material \
            WHERE id_materia = ? order by fecha_publicada;"
        self.cursor.execute(trabajos_sql, [ materia.id ])
        
        trabajos = []
        for f in self.cursor.fetchall():
            trabajos.append(Trabajo(f[0], f[1],f[2],f[3], f[4], f[5], materia, 
                                    f[7]))
        return trabajos


        

    def get_one(self, id_trabajo):
        rm = RepositorioMateria()
        trabajos_sql = "SELECT id, titulo, descripcion, fecha_publicada, \
                fecha_entrega, archivo, id_materia, es_url FROM material \
                WHERE id = ?;"
        self.cursor.execute(trabajos_sql, [id_trabajo])
        f = self.cursor.fetchone()
        materia = rm.get_one(f[6])
        trabajo = Trabajo(f[0], f[1],f[2],f[3], f[4], f[5], materia, f[7])
        return trabajo


    def get_trabajos_materia(self, materia):
        trabajos_sql = "SELECT id, titulo, descripcion, fecha_publicada, \
                fecha_entrega, archivo, id_materia, es_url \
                FROM material WHERE id_materia = ?;"
        self.cursor.execute(trabajos_sql, [ materia.id ])
        
        
        trabajos = []
        for f in self.cursor.fetchall():
            trabajos.append(Trabajo(f[0], f[1], f[2], f[3],f[4],f[5], materia, 
                                    f[7]))

        return trabajos

    def create(self, trabajo):
        insert = "INSERT INTO material (titulo, descripcion, fecha_publicada, \
                fecha_entrega, archivo, id_materia, es_url) \
                VALUES (?, ?, ?, ?, ?, ?, ?)"
        datos = [ trabajo.titulo, trabajo.descripcion, trabajo.publicado, 
          trabajo.entrega,trabajo.archivo,trabajo.materia.id,trabajo.es_url ]
        id_trabajo = self.cursor.execute(insert, datos)
        if not id_trabajo:
            return None
        else:
            self.bd.commit()
            return self.cursor.lastrowid


    def update(self, t):
        modificar_trabajo_sql = "UPDATE material SET titulo = ?,\
            descripcion = ?, fecha_publicada = ?, fecha_entrega = ?, \
            archivo = ?, id_materia = ?, es_url = ? WHERE id = ?"
        datos = [ t.titulo, t.descripcion, t.publicado, t.entrega, t.archivo, 
                  t.materia.id, t.es_url, t.id]
        if self.cursor.execute(modificar_trabajo_sql, datos):
            self.bd.commit()
            return True
        else:
            return False

    def delete(self, id_trabajo):
        # Si me pasan un objeto trabajo:
        if type(id_trabajo) is Trabajo:
            id_trabajo = id_trabajo.id

        borrar_sql = "DELETE FROM material WHERE id = ?"
        if self.cursor.execute(borrar_sql, [ id_trabajo ]):
            if self.cursor.rowcount == 1:
                self.bd.commit()
                return True
        return False








