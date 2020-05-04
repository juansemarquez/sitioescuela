#! /bin/bash
if [ $# -lt 3 ]
then
    echo "Error: necesito el usuario (y repositorio) de github, mail y clave"
    exit 11
fi
if [ ! -d sitio_para_subir ]
then
    echo "Hay que generar el sitio antes de subirlo"
    exit 12
fi
# cd sitio_para_subir && git init && git config user.name "$1" && git config user.email "$2" && git remote add origin https://github.com/$1/$1.github.io.git && git add . && git commit -m "Publicando el sitio, $(date)" && git push --force origin master
cd sitio_para_subir && (git init && git config user.name "$1" && git config user.email "$2" && git add . && git commit -m "Publicando el sitio, $(date)" && git push --force https://$1:$3@github.com/$1/$1.github.io.git master ) > /dev/null && echo "Sitio publicado correctamente"
exit $?
