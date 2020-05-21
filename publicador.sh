#! /bin/bash
if [ $# -lt 2 ]
then
    echo "Error: necesito el usuario (y repositorio) de github, y clave"
    exit 11
fi
if [ ! -d sitio_para_subir ]
then
    echo "Hay que generar el sitio antes de subirlo"
    exit 12
fi
# cd sitio_para_subir && git init && git config user.name "$1" && git config user.email "$2" && git remote add origin https://github.com/$1/$1.github.io.git && git add . && git commit -m "Publicando el sitio, $(date)" && git push --force origin master
cd sitio_para_subir
if [ ! -d .git ]
then
    if [ $# -lt 3 ]
    then
        echo "Error: Tenés que invocar al script: $0 tu-usuario-github tu-clave-github tu-email"
        exit 13
    else
        git init && config user.name "$1" && git config user.email "$3"
    fi
fi
(git add . && git commit -m "Publicando el sitio, $(date)" && git push https://$1:$2@github.com/$1/$1.github.io.git master ) > /dev/null && echo "Sitio publicado correctamente"
exit $?
