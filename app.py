#!/usr/bin/env python3
import sqlite3
from repositorio_curso import RepositorioCurso
from curso import Curso
from repositorio_materia import RepositorioMateria
from materia import Materia
from repositorio_trabajo import RepositorioTrabajo
from trabajo import Trabajo

from flask import Flask
from flask import render_template, request, redirect, url_for
from flaskwebgui import FlaskUI
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm

import datetime
import webbrowser
from threading import Timer

### PARA PERMITIR SUBIR ARCHIVOS ###
import os
from flask import flash 
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'material'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
                      'mp3', 'odt', 'ods', 'xls', 'xlsx', 'ppt', 'pptx', }
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ui = FlaskUI(app)


def allowed_file(filename):
    if not '.' in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
####################################

# app = Flask(__name__) (ya está en la parte de archivos)
csrf = CSRFProtect(app)
app.secret_key = b't\x97A\xca\x93<\x15\xf3\xdf\xbe\xf8G\xeeV\xda\xaa'
csrf.init_app(app)

@app.route("/")
def home():
    rc = RepositorioCurso()
    general = rc.get_general()
    if general[3]:
        return render_template("index.html", mensaje = None, hay_repo = True)
    else:
        return render_template("index.html", mensaje = None, hay_repo = False)


#################################################
##g CRUD DE LOS DATOS GENERALES DE LA ESCUELA ###
#################################################
@app.route("/general", methods = ["GET", "POST", "PUT"])
def general():
    if request.method == "GET":
        rc = RepositorioCurso()
        general = rc.get_general()
        if not general:
            return "Error: datos no encontrados."
        form = FlaskForm()
        return render_template("general.html",form=form, general = general)
    else:
        # Capturar los datos del request
        nombre = request.form["nombre"]
        numero = request.form["numero"]
        mail = request.form["mail"]
        tipo_hosting = request.form["tipo_hosting"]
        if tipo_hosting == "github":
            usuario= request.form["usuario_github"]
            clave = request.form["clave_github"]

        
        #HACER EL UPDATE
        rc = RepositorioCurso()
        if tipo_hosting == "github":
            if rc.actualizar_general(nombre, numero, mail, usuario, clave):
                mensaje = "Datos de la escuela y el proyecto modificados"
            else:
                mensaje = "Error al modificar los datos de la escuela"
        else: 
            if rc.actualizar_general(nombre, numero, mail):
                mensaje = "Datos de la escuela modificados"
            else:
                mensaje = "Error al modificar los datos de la escuela"
        #Redirigir a cursos: 
        return redirect(url_for('home', mensaje = mensaje))

#######################################
##c CRUD DE LOS DATOS DE LOS CURSOS ###
#######################################

@app.route("/cursos")
def cursos():
    if request.args.get("mensaje"):
        mensaje = request.args.get("mensaje")
    else:
        mensaje = None
    rc = RepositorioCurso()
    cursos = rc.get_all()
    form = FlaskForm()
    return render_template("cursos.html", mensaje = mensaje, cursos = cursos, 
            form=form)

@app.route("/cursos/nuevo", methods = ["GET", "POST"])
def create():
    if request.method == "GET":
        form = FlaskForm()
        return render_template("nuevo_curso.html", form = form, mensaje = None, 
                curso=None)
    else:
        # Capturar los datos del request 
        anio = request.form["anio"]
        division = request.form["division"]
        descripcion = request.form["descripcion"]
        curso = Curso(None, anio, division, descripcion)
        #GUARDAR EL NUEVO CURSO
        rc = RepositorioCurso()
        id_curso = rc.create(curso)
        if id_curso:
            mensaje = "Curso creado correctamente"
        else:
            mensaje = "Error al crear el curso"

        #Redirigir a cursos: 
        return redirect(url_for('cursos', mensaje = mensaje))

@app.route('/cursos/<int:id_curso>/edit', methods = ["GET", "PUT", "POST"])
def update(id_curso):
    rc = RepositorioCurso()
    if request.method == "GET":
        curso = rc.get_one(int(id_curso))
        if not curso:
            return "Error: curso no encontrado. id_curso: " + str(id_curso)
        form = FlaskForm()
        return render_template("nuevo_curso.html", mensaje = None, 
                                    form=form, curso = curso)
    else:
        # Capturar los datos del request
        id_c = request.form["id_curso"]
        anio = request.form["anio"]
        division = request.form["division"]
        descripcion = request.form["descripcion"]
        curso = Curso(id_c, anio, division, descripcion)
        #HACER EL UPDATE
        if rc.update(curso):
            mensaje = "Datos del curso modificados"
        else:
            mensaje = "Error al modificar los datos del curso"
        #Redirigir a cursos: 
        return redirect(url_for('cursos', mensaje = mensaje))

@app.route('/cursos/<int:id_curso>/delete', methods = ["DELETE", "POST"])
def delete(id_curso):
    # Hace el delete, verificando antes que no tenga materias guardadas
    rc = RepositorioCurso()
    if rc.cuantas_materias(id_curso) == 0:
        if rc.delete(id_curso):
            mensaje = "Curso eliminado"
        else:
            mensaje = "Error al eliminar el curso"
    else:
        mensaje = "Error: el curso tiene materias asignadas"

    #Redirigir a cursos: 
    return redirect(url_for('cursos', mensaje = mensaje))

#########################################
##m CRUD DE LOS DATOS DE LAS MATERIAS ###
#########################################

@app.route("/materias")
def materias(id_curso = None):
    rc = RepositorioCurso()
    cursos = rc.get_all()
    if request.args.get("mensaje"):
        mensaje = request.args.get("mensaje")
    else:
        mensaje = None
    rm = RepositorioMateria()
    if id_curso and int(id_curso) > 0:
        materias = rm.get_all_curso(id_curso)
        curso = rc.get_one(id_curso)
    else:
        materias = rm.get_all()
        curso = None
    form = FlaskForm()
    return render_template("materias.html", mensaje = mensaje, 
            materias = materias, form=form, cursos = cursos, curso = curso)

@app.route("/materias_por_curso/", methods= ["GET","POST"])
def materias_por_curso():
    id_curso = request.form["curso"]
    return materias(id_curso)

@app.route("/materias/nuevo", methods = ["GET", "POST"])
def create_materia(curso = None):
    if request.method == "GET":
        form = FlaskForm()
        rc = RepositorioCurso()
        cursos = rc.get_all()
        return render_template("nueva_materia.html", form = form, 
                mensaje = None, materia=None, cursos= cursos, curso = curso)
    else:
        # Capturar los datos del request 
        nombre = request.form["nombre"]
        id_curso = request.form["curso"]
        docente = request.form["docente"]
        mail = request.form["mail"]

        if request.form.get("sticky"):
            sticky = True
        else:
            sticky = False
        logo = request.form["logo"]
        rc = RepositorioCurso()
        curso = rc.get_one(id_curso)
        materia = Materia(None, nombre, curso, logo, sticky, docente, mail) 
        #GUARDAR EL NUEVO CURSO
        rm = RepositorioMateria()
        id_materia = rm.create(materia)
        if id_materia:
            mensaje = "Materia creada correctamente"
        else:
            mensaje = "Error al crear la materia"

        #Redirigir a cursos:        
        flash(mensaje)
        return materias(id_curso)

@app.route("/materias/nuevo/<int:id_curso>")
def create_materia_curso(id_curso):
    rc = RepositorioCurso()
    c = rc.get_one(id_curso)
    return create_materia(c)

@app.route("/materias/<int:id_materia>/edit", methods = ["GET", "POST", "PUT"])
def update_materia(id_materia):
    rm = RepositorioMateria()
    rc = RepositorioCurso()
    if request.method == "GET":
        cursos = rc.get_all()
        materia = rm.get_one(int(id_materia))
        if not materia:
            return "Error: materia no encontrada. id_materia: "+str(id_materia)
        form = FlaskForm()
        return render_template("nueva_materia.html", mensaje = None, 
                                    form=form,materia = materia, cursos=cursos)
    else:
        # Capturar los datos del request
        idm = request.form["id_materia"]
        nombre = request.form["nombre"]
        id_curso = request.form["curso"]
        docente = request.form["docente"]
        mail = request.form["mail"]
        if request.form.get("sticky"):
            sticky = True
        else:
            sticky = False
        if request.form.get("cambiar_logo"):
            logo = request.form["logo"]
        else:
            logo = None
        rc = RepositorioCurso()
        curso = rc.get_one(id_curso)
        materia = Materia(idm, nombre, curso, logo, sticky, docente, mail) 
        
        #HACER EL UPDATE
        if materia.logo:
            resultado = rm.update(materia)
        else:
            resultado = rm.update( materia , cambiar_logo = False) 
        if resultado:
            mensaje = "Datos de la materia modificados"
        else:
            mensaje = "Error al modificar los datos de la materia"
        #Redirigir a cursos: 
        return redirect(url_for('materias', mensaje = mensaje))

@app.route('/materias/<int:id_materia>/delete', methods = ["DELETE", "POST"])
def delete_materia(id_materia):
    # Hace el delete, verificando antes que no tenga trabajos guardados
    rm = RepositorioMateria()
    if rm.cuantos_trabajos(id_materia) == 0:
        if rm.delete(id_materia):
            mensaje = "Materia eliminada"
        else:
            mensaje = "Error al eliminar la materia"
    else:
        mensaje = "Error: la materia tiene trabajos asignados"

    #Redirigir a materias: 
    return redirect(url_for('materias', mensaje = mensaje))



#########################################
##t CRUD DE LOS DATOS DE LOS TRABAJOS ###
#########################################
@app.route("/trabajos")
def trabajos(id_materia = None):
    if request.args.get("mensaje"):
        mensaje = request.args.get("mensaje")
    else:
        mensaje = None
    rm = RepositorioMateria()
    rt = RepositorioTrabajo()
    if id_materia and int(id_materia) >  0:
        ts = rt.get_all_materia(id_materia)
        materia = rm.get_one(id_materia)
    else:
        ts = rt.get_all()
        materia = None
    materias = rm.get_all()
    form = FlaskForm()

    return render_template("trabajos.html", mensaje = mensaje, trabajos = ts,
            materias = materias, form=form, materia= materia)

@app.route("/trabajos_por_materia/", methods= ["POST"])
def trabajos_por_materia():
    id_materia = request.form["materia"]
    return trabajos(id_materia)


@app.route("/trabajos/nuevo", methods = ["GET", "POST"])
def create_trabajos(materia = None):
    rm = RepositorioMateria()
    if request.method == "GET":
        hoy = datetime.date.today()
        form = FlaskForm()
        materias = rm.get_all()
        return render_template("nuevo_trabajo.html", form = form, mensaje=None, 
                          trabajo=None, materias = materias, materia = materia, 
                          hoy=hoy,tipos = ", ".join(ALLOWED_EXTENSIONS))
    else:
        # Capturar los datos del request
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        id_materia = request.form["materia"]
        # TODO: Las fechas tienen que ser "2020-04-30", revisar eso
        fecha_publicada = request.form["publicado"]
        if request.form.get("se_entrega"):
            fecha_entrega = request.form["entrega"]
        else:
            fecha_entrega = None
        es_url = request.form["opcion_archivo"] == "url"
        materia = rm.get_one(id_materia)
        
        # Manejo de archivos:
        # print("################### ARCHIVOS ##########################")
        # print(request.files.get("archivo_real").filename)
        if 'archivo_real' in request.files:
            archivo_real = request.files['archivo_real']
        
            # FIXME: ¿Habría que advertir si eligen archivo pero no suben nada?
            # (ya está hecho por js)
            # if archivo_real.filename == '':
            if archivo_real and allowed_file(archivo_real.filename):
                filename = secure_filename(archivo_real.filename)
                archivo = filename
                try:
                    archivo_real.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                                   filename))
                except:
                    #FIXME: Manejar esta excepción. TODO
                    raise
            else:
                # FIXME: Manejar esta excepción
                raise
        else:
            archivo = request.form["archivo"]
        
        
        trabajo = Trabajo(None, titulo, descripcion, fecha_publicada, 
                            fecha_entrega, archivo, materia, es_url)


        #GUARDAR EL NUEVO TRABAJO
        rt = RepositorioTrabajo()
        id_trabajo = rt.create(trabajo)
        if id_trabajo:
            mensaje = "Trabajo/Material/Actividad creada correctamente"
        else:
            mensaje = "Error al crear el trabajo"

        #Redirigir a trabajos: 
        return redirect(url_for('trabajos', mensaje = mensaje))

@app.route("/trabajos/nuevo/<int:id_materia>")
def create_trabajos_materia(id_materia):
    rm = RepositorioMateria()
    m = rm.get_one(id_materia)
    return create_trabajos(m)

@app.route("/trabajos/<int:id_trabajo>/edit", methods = ["GET", "POST", "PUT"])
def update_trabajos(id_trabajo):
   rm = RepositorioMateria()
   rt = RepositorioTrabajo()
   trabajo_actual = rt.get_one(int(id_trabajo))
   
   if request.method == "GET":
        if not trabajo_actual:
            return "Error: trabajo no encontrada. id_trabajo: "+str(id_trabajo)
        hoy = datetime.date.today()
        form = FlaskForm()
        materias = rm.get_all()
        return render_template("nuevo_trabajo.html", form = form, mensaje=None, 
                trabajo=trabajo_actual, materias = materias, hoy=hoy)
   else:
        # Capturar los datos del request 
        idt = request.form["id_trabajo"]
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        id_materia = request.form["materia"]
        fecha_publicada = request.form["publicado"]
        if request.form.get("se_entrega"):
            fecha_entrega = request.form["entrega"]
        else:
            fecha_entrega = None
        es_url = request.form["opcion_archivo"] == "url"
        materia = rm.get_one(id_materia)
        
        # Manejo de archivos:
        if 'archivo_real' in request.files and \
                request.form["archivo"] != trabajo_actual.archivo:
            archivo_real = request.files['archivo_real']
        
            # FIXME: ¿Habría que advertir si eligen archivo pero no suben nada?
            # (ya está hecho por js)
            # if archivo_real.filename == '':
            if archivo_real and allowed_file(archivo_real.filename):
                filename = secure_filename(archivo_real.filename)
                archivo = filename
                try:
                    archivo_real.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                                   filename))
                except:
                    #FIXME: Manejar esta excepción. TODO
                    raise
            else:
                # FIXME: Manejar esta excepción
                raise
        else:
            archivo = request.form["archivo"]
        
        
        trabajo = Trabajo(idt, titulo, descripcion, fecha_publicada, 
                            fecha_entrega, archivo, materia, es_url)


        #HACER EL UPDATE
        resultado = rt.update(trabajo)
        if resultado:
            mensaje = "Datos del trabajo/actividad/material modificados"
        else:
            mensaje = "Error al modificar los datos del trabajo/material"
        #Redirigir a cursos: 
        return redirect(url_for('trabajos', mensaje = mensaje))

@app.route('/trabajos/<int:id_trabajo>/delete', methods = ["DELETE", "POST"])
def delete_trabajos(id_trabajo):
    # Hace el delete 
    rt = RepositorioTrabajo()
    if rt.delete(id_trabajo):
        mensaje = "Actividad/trabajo/material eliminada"
    else:
        mensaje = "Error al eliminar la actividad/trabajo/material"

    #Redirigir a materias: 
    return redirect(url_for('trabajos', mensaje = mensaje))

#################################################
###  EJECUTAR EL GENERADOR DE SITIO ESTÁTICO  ###
#################################################
@app.route('/generador')
def dale():
    # exec(open("generador.py").read())
    from generador import generar
    flash(generar())
    return redirect(url_for('home'))

@app.route('/subir')
def subir():
    import subprocess
    rc = RepositorioCurso()
    general = rc.get_general()
    if general[2] and general[3] and general[4]:
        x =subprocess.run(["./publicador.sh",general[3],general[2],general[4]], 
                stdout=subprocess.PIPE, encoding="utf-8")
        flash(x.stdout)
        return redirect(url_for('home'))
    else:
        flash("Error: sin mail, usuario o contraseña para subir el sitio")
        return redirect(url_for('home'))

def open_browser():
      webbrowser.open_new('http://127.0.0.1:2345/')

if __name__=="__main__":
    # Timer(1,open_browser).start()
    ui.run()
    # app.run(debug=False, port=2345)
