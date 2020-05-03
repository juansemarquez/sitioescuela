function verCurso(id_curso) {
    window.location.href = id_curso;
}

function verTrabajos(id_materia)
{
    window.scrollTo({ top: 140 });
    id = "trabajos" + id_materia;
    const v = document.getElementById(id);
    v.classList.add('trabajos_activo');
    v.classList.remove('trabajos_inactivo');
    document.querySelector("#encabezado").classList.add('blureado');
    document.querySelectorAll(".materia").forEach( function (e) {
        e.classList.add('blureado');
    });
    v.style.filter = "none";
    window.onclick = function(event) {
        var t = event.target;
        console.log(t)
        if (t == v) {
            cerrarTrabajos(id)
        }
    }
    /*
    const el = document.querySelector("#contenedor").childNodes;
    console.log(el);
    el.forEach(function(e) {
        if (!e.classList.contains("trabajos_activo")) {
            e.classList.add('blureado');
        }
    });
    */

}

function cerrarTrabajos(id_materia) {
    id = "trabajos" + id_materia;
    v = document.getElementById(id);
    v.classList.add('trabajos_inactivo');
    v.classList.remove('trabajos_activo');
    document.querySelector("#encabezado").classList.remove('blureado');
    document.querySelectorAll(".materia").forEach( function (e) {
        e.classList.remove('blureado');
    });
}




