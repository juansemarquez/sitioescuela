#! /usr/bin/env python3
import sqlite3
from materia import Materia
from curso import Curso
from trabajo import Trabajo
class RepositorioMateria:
    def __init__(self):
        self.bd = sqlite3.connect("bd.sqlite")
        self.bd.row_factory = sqlite3.Row
        self.cursor = self.bd.cursor()

    def get_all(self):
        materias_sql = "SELECT m.id, m.nombre, \
                c.anio, c.division, c.descripcion, c.id, \
                m.docente, m.sticky, m.logo, m.mail \
                FROM materias m JOIN cursos c ON m.curso = c.id \
                ORDER BY m.curso, sticky DESC;" 
        self.cursor.execute(materias_sql)
        materias = []

        for row in self.cursor.fetchall():
            curso = Curso(row[5], row[2],row[3],row[4])
            materia = Materia(row[0],row[1],curso,row[8],row[7],row[6],row[9])
            materias.append(materia)
        return materias

    def get_one(self, id_materia):
        materias_sql = "SELECT m.id, m.nombre, \
                c.anio, c.division, c.descripcion, c.id, \
                m.docente, m.sticky, m.logo, m.mail \
                FROM materias m JOIN cursos c ON m.curso = c.id \
                WHERE m.id = ?"
        self.cursor.execute(materias_sql, [ id_materia ])
        for row in self.cursor.fetchall():
            curso = Curso(row[5], row[2],row[3],row[4])
            materia = Materia(row[0],row[1],curso,row[8],row[7],row[6],row[9])
            return materia
        return None

    def get_all_curso(self, id_curso):
        #Si me pasan un curso en vez de un id:
        if type(id_curso) is Curso:
            id_curso = id_curso.id

        materias_sql = "SELECT m.id, m.nombre, \
                c.anio, c.division, c.descripcion, c.id, \
                m.docente, m.sticky, m.logo, m.mail \
                FROM materias m JOIN cursos c ON m.curso = c.id \
                WHERE m.curso = ? \
                ORDER BY m.curso, sticky DESC;" 
        self.cursor.execute(materias_sql, [ id_curso ])
        materias = []

        for row in self.cursor.fetchall():
            curso = Curso(row[5], row[2],row[3],row[4])
            materia = Materia(row[0],row[1],curso,row[8],row[7],row[6],row[9])
            materias.append(materia)
        return materias

    def get_trabajos_materia(self, materia):
        trabajos_sql = "SELECT id, titulo, descripcion, fecha_publicada, \
                fecha_entrega, archivo \
                FROM material WHERE id_materia = ?;"
        self.cursor.execute(trabajos_sql, [ materia ])
        trabajos = []

        for f in self.cursor.fetchall():
            trabajos.append(Trabajo(f[0], f[1], f[2], f[3], f[4], f[5]))

        return trabajos

    def get_all_con_trabajos(self):
        #FIXME: Agregar el docente y el mail
        materias_con_trabajos_sql = "SELECT m.id, m.nombre, c.descripcion, \
                MAX(t.fecha_publicada), COUNT(t.id) \
                FROM materias m JOIN cursos c ON m.curso = c.id \
                LEFT JOIN material t ON t.id_materia = m.id \
                GROUP BY m.id ORDER BY c.id"
        self.cursor.execute(materias_con_trabajos_sql)
        materias = []
        for m in self.cursor.fetchall():
            materias.append( [ m[0], m[1], m[2], m[3], m[4] ] )
        return materias


    def create(self, materia):
        insert = "INSERT INTO materias(nombre,curso,docente,sticky,logo,mail) \
                VALUES ( ? , ?, ?, ?, ?, ?)"
        datos = [ materia.nombre, materia.curso.id, materia.docente, 
                materia.sticky, materia.logo, materia.mail ]
        self.cursor.execute(insert, datos)
        self.bd.commit()
        return self.cursor.lastrowid

    def update(self, m, cambiar_logo = True):
        if cambiar_logo:
            modificar_materia_sql = "UPDATE materias SET nombre = ?,curso = ?, \
                docente = ?, sticky = ?, logo = ?, mail = ? WHERE id = ?"
            datos = [m.nombre,m.curso.id,m.docente,m.sticky,m.logo,m.mail,m.id]
        else:
            modificar_materia_sql = "UPDATE materias SET nombre = ?,curso = ?, \
                docente = ?, sticky = ?, mail = ? WHERE id = ?"
            datos = [m.nombre, m.curso.id, m.docente, m.sticky, m.mail, m.id ]
        if self.cursor.execute(modificar_materia_sql,datos):
            self.bd.commit()
            return True
        else:
            return False


    def cuantos_trabajos(self, id_materia):
        #Si me mandaron un objeto en vez de un id:
        if type(id_materia) is Materia:
            id_materia = id_materia.id

        contar_trabajos_sql="SELECT COUNT(id) FROM material WHERE id_materia=?"
        self.cursor.execute(contar_trabajos_sql, [ id_materia ] )
        return self.cursor.fetchone()[0]

    def delete(self, id_materia):
        # Si me pasan un objeto materia:
        if type(id_materia) is Materia:
            id_materia = id_materia.id

        borrar_sql = "DELETE FROM materias WHERE id = ?"
        if self.cursor.execute(borrar_sql, [ id_materia ]):
            if self.cursor.rowcount == 1:
                self.bd.commit()
                return True
        return False

