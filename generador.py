#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import getopt, sys
import shutil, os
import pathlib
import sqlite3
import datetime
from jinja2 import Environment, PackageLoader  
from curso import Curso
from repositorio_generador import RepositorioGenerador
from repositorio_curso import RepositorioCurso

def falta_archivo(archivo, trabajo=None, materia=None, curso=None):
    '''Esta función se invoca antes de lanzar la excepción por la falta de
    un archivo'''
    error = f"Falta el archivo {archivo}" 
    if trabajo:
        error += f" del trabajo {trabajo.titulo} de {materia.nombre}"
        error += f" de {curso}"
    error += ". No subas nada, que se rompió."
    if os.path.isdir('sitio_para_subir'):
        shutil.rmtree('sitio_para_subir')
    return error



def generar(parametros = None):

    import getopt, sys
    import shutil, os
    import pathlib
    import sqlite3
    import datetime
    from jinja2 import Environment, PackageLoader  
    from curso import Curso
    from repositorio_generador import RepositorioGenerador


    ahora = datetime.datetime.now()

    rg = RepositorioGenerador()
    escuela = rg.get_datos_escuela()
    todos_los_cursos = rg.get_all()

    if not parametros:
        cursos = todos_los_cursos
    else:
        cursos = []
        for p in parametros:
            cursos.append(rg.get_one_curso(int(p)))

    if os.path.isdir('sitio_para_subir'):
        # shutil.rmtree('sitio_para_subir')
        os.rename('sitio_para_subir','sps')
        if os.path.isdir('sps/.git'):
            try:
                os.mkdir('sitio_para_subir')
                shutil.copytree('sps/.git','sitio_para_subir/.git')
            except:
                os.rename('sps', 'sitio_para_subir')
                return falta_archivo('sps/.git')
        shutil.rmtree('sps')
        
    # else:
        # try:
            # os.mkdir('sitio_para_subir')
            #os.chdir('sitio_para_subir')
            # print(os.getcwd())
            # subprocess.check_call(['git'] + ['init'])
            # rc = RepositorioCurso()
            # general = rc.get_general()
            # subprocess.check_call(['git'] + ['config','user.name', general[3]])
            # subprocess.check_call(['git'] + ['config','user.email',general[2]]) 
            # os.chdir('..')
            # print(os.getcwd())
        # except:
            # return falta_archivo('No pude iniciar el nuevo repositorio')

    carpeta = 'sitio_para_subir/static/fuentes'
    pathlib.Path(carpeta).mkdir(parents=True, exist_ok=True)

    carpeta = 'sitio_para_subir/static/logos'
    pathlib.Path(carpeta).mkdir(parents=True, exist_ok=True)

    lista_archivos = [ 'static/estilo.css', 
                       'static/logo.png',
                       'static/scripts.js',
                       'static/fuentes/Comfortaa-Bold.ttf',
                       'static/fuentes/Comfortaa-Light.ttf',
                       'static/fuentes/Comfortaa-Regular.ttf'
                     ]
    for origen in lista_archivos:
        try:
            shutil.copy2(origen, 'sitio_para_subir/' + origen)
        except:
            return falta_archivo(origen)
            

    # Generamos la página incial:
    datos = { 'numero_escuela': escuela['numero'],
              'nombre_escuela': escuela['nombre'],
              'mail_escuela': escuela['mail'],
              'cursos' : todos_los_cursos,
              'ahora':ahora, 
            }
    env = Environment(loader=PackageLoader('generador', 'templates'))

    template = env.get_template('generador-index.html')
    x = template.render(datos = datos)    
    with open('sitio_para_subir/index.html', 'w', encoding='utf-8') as file:
        file.write(x)

    # Generamos las páginas de todos los cursos/grados:
    for c in cursos:
        print("Generando la página del curso ", str(c.anio), c.division)
        materias = rg.get_all_curso( c )
        #carpeta = str(escuela['numero']) + '/' + str(c.anio) + c.division
        carpeta = 'sitio_para_subir/' + str(c.id)
        pathlib.Path(carpeta).mkdir(parents=True, exist_ok=True)
    
        #Copiar los archivos necesarios:
        for m in materias:
            logo = 'static/logos/' + m.logo
            destino = 'sitio_para_subir/static/logos/'
            try:
                shutil.copy2(logo, destino)
            except:
                return falta_archivo(logo)
            for t in m.lt:
                if not t.es_url:
                    origen = 'material/' + t.archivo
                    destino = 'sitio_para_subir/'+str(c.id)+'/'
                    try:
                        shutil.copy2(origen, destino)
                    except:
                        return falta_archivo(origen, t, m, c)
        #cd = str(c.anio) + c.division
        datos = { 'numero_escuela': escuela['numero'],
                  'nombre_escuela': escuela['nombre'],
                  'mail_escuela': escuela['mail'],
                  'curso': c,
                  'materias': materias, 
                  'ahora':ahora, 
                  }
        env = Environment(loader=PackageLoader('generador', 'templates'))
      
        template = env.get_template('generador.html')
        x = template.render(datos = datos)    
        with open("sitio_para_subir/"+str(c.id)+'/index.html', 
                  'w', encoding='utf-8') as file:
            file.write(x)
    return "El sitio se ha generado con éxito"

if __name__ == '__main__':
    parametros = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])[1]
    print(parametros)
    generar(parametros)
