webapp_host = "http://localhost:5000";

// Obtener todos los mensajes de IoT en UI
function fetchMensajesIoT() {
    fetch(webapp_host+"/mensajes-iot")
    .then(response => response.json()) // Convertir respuesta como JSON
    .then(data => {
        var labelElement = document.getElementById("totalMensajes");
        labelElement.textContent = data?.total
    })
    .catch(error => console.error('Error:', error)); // Registrar errores en consola
}

// Obtener los registros más altos hoy
function fetchRegistrosAltos() {
    fetch(webapp_host + "/registros-altos-hoy")
        .then((response) => response.json()) // Convertir respuesta como JSON
        .then((data) => {
            let tbody = document.getElementById("tbodyRegistrosAltos")
            tbody.innerHTML = ''
            data.registros.forEach((item) => {
                let row = document.createElement("tr");

                for (let property in item) {
                    let cell = document.createElement("td");

                    if (property == 1) {
                        // Cuando el valor registrado de temperatura es mayor a 130, visualizar color rojo
                        if (item[property] > 130) {
                            cell.style.color="red"
                        }
                    }
                    cell.textContent = item[property];
                    row.appendChild(cell);
                }

                // Adjuntar registro al cuerpo de la tabla
                tbody.appendChild(row);
            });
        })
        .catch((error) => console.error("Error:", error)); // Registrar errores en consola
}

// Código que sucede cuando el documento HTML esta cargado
document.addEventListener("DOMContentLoaded", () => {

    // Cargar información la primera vez
    fetchMensajesIoT()
    fetchRegistrosAltos();

    // Intervalos para refrescar constantemente la información de los componentes
    let intervaloMensajes = setInterval(fetchMensajesIoT, 2500);
    let intervaloRegistros = setInterval(fetchRegistrosAltos, 15000);
});
