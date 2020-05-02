# sitioescuela
Un sitio Web para tu escuela, gratis y sin escribir código. Seguimos educando aun en la pandemia.

## Funcionamiento:
- Un crud en Flask para cargar una Base de datos sqlite (suena difícil, pero es fácil: solamente hay que escribir los nombres de las materias, de los docentes de tu escuela, etc).
- Un generador estático que crea el sitio en HTML ¡Sin escribir código!
- Si querés, lo subís a cualquier servidor. Y si la escuela no tiene hosting, se "sube" solo a GitHub Pages (próximamente).
- ¡Listo! Tu escuela ya tiene sitio Web.
Seguimos educando hasta que pase el CoViD-19- #Quedateencasa

## ¿Y cómo va a quedar el sitio?
**¿Hay demo?** Hay demo: https://juansemarquez.github.io/sitioescuela_demo

## Instalación

### Antes de empezar

> :warning: `sitioescuela` corre con python 3.6 o superior. Si tenés mas de una instalación de python, lee esta sección. De lo contrario, podés ignorarla.

Para poder usar python3 por defecto con `sitioescuela` instalá primero `venv`:

```bash
$ python3 -m venv venv
```

Ahora, cada vez que te muevas dentro del directorio del proyecto, vas a tener que ejecutar el siguiente comando:

```bash
$ . venv/bin/activate
```

### Dependencias

Por única vez, ejecutá el siguiente comando:

```bash
$ python -m pip install flask flask_wtf
```

`sitioescuela` también utiliza `tkinter`. Asegurate de que tu sistema tenga instalado el paquete `python3-tk` o similar.

## Uso

Para empezar a usar `sitioescuela`, ejecutá:

```bash
$ flask run
```

Se iniciará un servidor en `http://127.0.0.1:5000/`. Desde ahí vas a poder:

1. Actualizar los datos de tu escuela
2. Generar y mantener los cursos, materiales y actividades
3. Generar un sitio estático que podés subir por ejemplo a [github pages](https://pages.github.com/). El sitio se generará en el directorio `sitio_para_subir/`

## Créditos:
- A todos los docentes, por su esfuerzo, vocación y profesionalismo para seguir educando en este difícil momento.
- A todos los pibes y las pibas, que se tienen que quedar en casa. Gracias por darnos el ejemplo de que se puede aprender siempre, sin perder la alegría.
- A toda la comunidad del Software Libre en general, y de Python en particular.
- Los "logos" que le podés poner a las materias, son gracias al trabajo generoso de [este artista](https://illlustrations.co/)
