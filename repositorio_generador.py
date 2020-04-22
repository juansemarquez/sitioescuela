#! /usr/bin/env python3
import sqlite3
from materia_con_trabajos import MateriaConTrabajos
from curso import Curso
from trabajo import Trabajo
class RepositorioGenerador:
    def __init__(self):
        self.bd = sqlite3.connect("bd.sqlite")
        self.bd.row_factory = sqlite3.Row
        self.cursor = self.bd.cursor()

    def get_datos_escuela(self):
        sql = "SELECT nombre_escuela,numero_escuela,mail_contacto FROM general"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        datos_escuela = { 'nombre': row[0], 'numero': row[1], 'mail':row[2] }
        return datos_escuela

    def get_all(self):
        cursos_sql = "SELECT id, anio, division, descripcion FROM cursos";
        self.cursor.execute(cursos_sql)
        cursos = []
        for row in self.cursor.fetchall():
            cursos.append(Curso(row[0], row[1], row[2], row[3] ))
        return cursos

    def get_one_curso(self, id_curso):
        sql = "SELECT id,anio,division,descripcion FROM cursos WHERE id=?";
        self.cursor.execute(sql, [ id_curso ])
        row = self.cursor.fetchone()
        return Curso(row[0], row[1], row[2], row[3])

    def get_all_curso(self, curso):
        materias_sql="SELECT m.id,m.nombre,MAX(t.fecha_publicada) as ultima,\
                COUNT(t.id) as cantidad,m.docente, m.sticky, m.logo, m.mail \
                FROM materias m LEFT JOIN material t ON t.id_materia = m.id \
                WHERE m.curso = ? GROUP BY m.id ORDER BY sticky DESC;" 
        self.cursor.execute(materias_sql, [curso.id])
        materias = []

        for row in self.cursor.fetchall():
            trabajos = self.get_trabajos_materia(row[0]) 
            m = MateriaConTrabajos(row[0], row[1], row[2], row[3], row[4],
                                   row[5], row[6], row[7])
            m.cargar_trabajos(trabajos)
            materias.append(m)

        return materias


    def get_trabajos_materia(self, materia):
        trabajos_sql = "SELECT id, titulo, descripcion, fecha_publicada, \
                fecha_entrega, archivo, es_url \
                FROM material WHERE id_materia = ?;"
        self.cursor.execute(trabajos_sql, [ materia ])
        trabajos = []

        for f in self.cursor.fetchall():
            url = (int(f[6]) == 1)
            trabajos.append(Trabajo(f[0],f[1],f[2],f[3],f[4],f[5],None,url))

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


