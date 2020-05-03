#! /bin/bash
if [ $# -lt 1 ]
then
    echo "Error: necesito el usuario (y repositorio) de github"
    exit 11
fi
if [ ! -d sitio_para_subir ]
then
    echo "Hay que generar el sitio antes de subirlo"
    exit 12
fi
cd sitio_para_subir && git init && git config user.name "$1" && git config user.email "sitioescuela@juansemarquez.com" && git remote add origin https://github.com/$1/$1.github.io.git && git add . && git commit -m "Publicando el sitio, $(date)" && git push --force origin master
exit $?
