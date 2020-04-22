#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import getopt, sys
import shutil
import pathlib
import sqlite3
import datetime
from jinja2 import Environment, PackageLoader  
from curso import Curso
from repositorio_generador import RepositorioGenerador

parametros = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])[1]
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

carpeta = str(escuela['numero']) + '/static/fuentes'
pathlib.Path(carpeta).mkdir(parents=True, exist_ok=True)
carpeta = str(escuela['numero']) + '/static/logos'
pathlib.Path(carpeta).mkdir(parents=True, exist_ok=True)
lista_archivos = [ 'static/estilo.css', 
                   'static/logo.png',
                   'static/scripts.js',
                   'static/fuentes/Comfortaa-Bold.ttf',
                   'static/fuentes/Comfortaa-Light.ttf',
                   'static/fuentes/Comfortaa-Regular.ttf'
                 ]
for origen in lista_archivos:
    shutil.copy2(origen, str(escuela['numero']) + '/' + origen)

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
with open(str(escuela['numero']) + '/index.html', 
    'w', encoding='utf-8') as file:
    file.write(x)




# Generamos las páginas de todos los cursos/grados:
for c in cursos:
    materias = rg.get_all_curso( c )
    #carpeta = str(escuela['numero']) + '/' + str(c.anio) + c.division
    carpeta = str(escuela['numero']) + '/' + str(c.id)
    pathlib.Path(carpeta).mkdir(parents=True, exist_ok=True)
    
    #Copiar los archivos necesarios:
    for m in materias:
        logo = 'static/logos/' + m.logo
        destino = str(escuela['numero']) + '/static/logos/'
        shutil.copy2(logo, destino)
        for t in m.lt:
            if not t.es_url:
                origen = 'material/' + t.archivo
                destino = str(escuela['numero'])+'/'+str(c.anio)+c.division+'/'
                shutil.copy2(origen, destino)
    #cd = str(c.anio) + c.division
    cd = str(c.id)
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
    with open(str(escuela['numero'])+"/"+cd+'/index.html', 
              'w', encoding='utf-8') as file:
        file.write(x)
