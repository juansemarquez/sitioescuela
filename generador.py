#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import getopt, sys
import shutil, os
import pathlib
import sqlite3
import datetime
import tkinter
from jinja2 import Environment, PackageLoader  
from curso import Curso
from repositorio_generador import RepositorioGenerador

def falta_archivo(archivo):
    '''Esta función se invoca antes de lanzar la excepción por la falta de
    un archivo'''
    error = f"Falta el archivo {origen}. No subas nada, que se rompió."
    print("Error: "+error)
    # tkinter.messagebox.showerror(title=None, message=error, **options)
    root = tkinter.Tk()
    root.title("¡Epa!")
    label = tkinter.Label(root, text=error)
    label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
    button = tkinter.Button(root, text="De acuerdo, lo voy a revisar", 
                command=lambda: root.destroy())
    button.pack(side="bottom", fill="none", expand=True)
    root.mainloop()
    if os.path.isdir('sitio_para_subir'):
        shutil.rmtree('sitio_para_subir')


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

if os.path.isdir('sitio_para_subir'):
    shutil.rmtree('sitio_para_subir')

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
        falta_archivo(origen)
        raise

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
            falta_archivo(logo)
            raise
        for t in m.lt:
            if not t.es_url:
                origen = 'material/' + t.archivo
                destino = 'sitio_para_subir/'+str(c.id)+'/'
                try:
                    shutil.copy2(origen, destino)
                except:
                    falta_archivo(origen)
                    raise
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
