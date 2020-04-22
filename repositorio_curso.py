#! /usr/bin/env python3
import sqlite3
from curso import Curso
class RepositorioCurso:
    def __init__(self):
        self.bd = sqlite3.connect("bd.sqlite")
        self.bd.row_factory = sqlite3.Row
        self.cursor = self.bd.cursor()

    def get_all(self):
        cursos_sql = "SELECT id, anio, division, descripcion FROM cursos";
        self.cursor.execute(cursos_sql)
        cursos = []
        for row in self.cursor.fetchall():
            cursos.append(Curso(row[0], row[1], row[2], row[3] ))
        return cursos

    def get_one(self, id_curso):
        cursos_sql = "SELECT id, anio, division, descripcion FROM cursos WHERE id=?";
        self.cursor.execute(cursos_sql, [ id_curso ])
        row = self.cursor.fetchone()
        return Curso(row[0], row[1], row[2], row[3])
        #if type(row) is tuple:
        #    return Curso(row[0], row[1], row[2], row[3])
        #else:
        #    return None

    def create(self, curso):
        crear_curso_sql = "INSERT INTO cursos (anio, division, descripcion) \
                VALUES (?,?,?)"
        id = self.cursor.execute(crear_curso_sql, 
                [ curso.anio, curso.division, curso.descripcion ] )
        if not id:
            return None
        else:
            self.bd.commit()
            return self.cursor.lastrowid

    def update(self, curso):
        modificar_curso_sql = "UPDATE cursos SET anio = ?, division = ?, \
                descripcion = ? WHERE id = ?"
        if self.cursor.execute(modificar_curso_sql,
                [ curso.anio, curso.division, curso.descripcion, curso.id ] ):
            self.bd.commit()
            return True
        else:
            return False

    def cuantas_materias(self, id_curso):
        #Si me mandaron un curso en vez de un id:
        if type(id_curso) is Curso:
            id_curso = id_curso.id

        contar_materias_sql = "SELECT COUNT(id) FROM materias WHERE curso = ?"
        self.cursor.execute(contar_materias_sql, [ id_curso ] )
        return self.cursor.fetchone()[0]
    

    def delete(self, id_curso):
        #Si me mandaron un curso en vez de un id:
        if type(id_curso) is Curso:
            id_curso = id_curso.id
            
        borrar_curso_sql = "DELETE FROM cursos WHERE id = ?"
        if self.cursor.execute(borrar_curso_sql, [ id_curso ]):
            if self.cursor.rowcount == 1:
                self.bd.commit()
                return True
        return False

    def get_general(self):
        general_sql = "SELECT nombre_escuela, numero_escuela, mail_contacto \
                FROM general;"
        self.cursor.execute(general_sql)
        row = self.cursor.fetchone()
        return row

    def actualizar_general(self, nom, num = None, mail = None):
        if not num and not mail:
            general_sql = "UPDATE general SET nombre_escuela = ?, \
                numero_escuela = NULL, mail_contacto = NULL WHERE id=1"
            datos = [ nom ]
        elif not num:
            general_sql = "UPDATE general SET nombre_escuela = ?, \
                numero_escuela = NULL, mail_contacto = ? WHERE id=1"
            datos = [ nom, mail ]
        elif not mail:
            general_sql = "UPDATE general SET nombre_escuela = ?, \
                numero_escuela = ?, mail_contacto = NULL WHERE id=1"
            datos = [ nom, num ]
        else:
            general_sql = "UPDATE general SET nombre_escuela = ?, \
                numero_escuela = ?, mail_contacto = ? WHERE id=1"
            datos = [ nom, num, mail ]

        if self.cursor.execute(general_sql, datos):
            self.bd.commit()
            return True
        else:
            return False

    def get_all_diccionario(self, reverso = False):
        '''Esto es para poblar los combobox. 
        Un asco, tiene que haber otra manera'''
        cursos = self.get_all()
        diccionario = {}
        secuencial = 0
        for c in cursos:
            if reverso:
                diccionario.update({ c.id : secuencial })
            else: 
                diccionario.update({ secuencial : c.id })
            secuencial += 1
        return diccionario

    def get_all_descripciones(self):
        cursos = self.get_all()
        lista = []
        for c in cursos:
            lista.append(c.descripcion)
        return lista
                    
        
        

        




