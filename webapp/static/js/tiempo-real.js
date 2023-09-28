const TOPICOS = {
    TEMPERATURAS: "iot/temperaturas",
};

const IOT_TAGS = {
    TEMPERATURAS: {
        MAQUINA_A: "maquina_a.temperatura",
        MAQUINA_B: "maquina_b.temperatura",
    },
};

var ctx = document
    .getElementById("graficasSensoresTiempoReal")
    .getContext("2d");

let realtimeSensoresChart;

function convertirUTC(marcaDeTiempo) {
    let fecha = new Date(marcaDeTiempo);
    console.log("fecha.getHours()", fecha.getHours());

    fecha.setHours(fecha.getHours() - 6);
    return fecha;
}

var labelTopico = document.getElementById("topico");
var labelMensaje = document.getElementById("mensaje");
var labelMarcaDeTiempo = document.getElementById("marcaDeTiempo");

Chart.register(ChartDataLabels);

realtimeSensoresChart = new Chart(ctx, {
    type: "line",
    data: {
        datasets: [
            {
                id: IOT_TAGS.TEMPERATURAS.MAQUINA_A,
                label: IOT_TAGS.TEMPERATURAS.MAQUINA_A,
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                borderColor: "rgba(255, 99, 132, 1)",
                data: [],
                pointStyle: "circle",
                pointRadius: 20,
                pointHoverRadius: 20,
                fill: true,
                tension: 0.4,
            },
            {
                id: IOT_TAGS.TEMPERATURAS.MAQUINA_B,
                label: IOT_TAGS.TEMPERATURAS.MAQUINA_B,
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                borderColor: "rgba(75, 192, 192, 1)",
                data: [],
                pointStyle: "circle",
                pointRadius: 20,
                pointHoverRadius: 20,
                fill: true,
                tension: 0.4,
            },
        ],
    },
    options: {
        responsive: true,
        scales: {
            x: {
                type: "realtime",
                realtime: {
                    duration: 25000,
                },
                stacked: true,
            },
            y: {
                stacked: true,
                min: 0,
                max: 135,
            },
        },
        layout: {
            padding: {
                top: 10,
            },
        },
        plugins: {
            datalabels: {
                formatter: function (value, context) {
                    return value.y;
                },
            },
            legend: {
                position: "bottom",
            },
        },
    },
});

// Conexión del broker utilizando el protocolo websocket (ws)
const WEBSOCKET_URL = "ws://localhost:9001";
const client = mqtt.connect(WEBSOCKET_URL);

// Código que sucede cuando el documento HTML esta cargado
document.addEventListener("DOMContentLoaded", () => {
    client.on("connect", function () {
        console.log("Connected");

        client.subscribe(TOPICOS.TEMPERATURAS);
    });

    // Evento cada vez que llega un nuevo mensaje al broker MQTT relacionado a los tópicos suscritos
    client.on("message", function (topic, message) {
        const payload = JSON.parse(message.toString());
        let fechaLocal = convertirUTC(payload.marcaDeTiempo);

        labelTopico.textContent = 'topico: ' + topic;
        labelMensaje.textContent = message.toString();
        labelMarcaDeTiempo.textContent = 'fecha: ' + fechaLocal.toLocaleString('es-MX', { dateStyle: 'short', timeStyle: 'medium' });

        if (topic === TOPICOS.TEMPERATURAS) {
            // Actualizar gráfico en tiempo-real
            realtimeSensoresChart.data.datasets.forEach((dataset) => {
                if (dataset.id === payload.sensor) {
                    dataset.data.push({ x: fechaLocal, y: payload.valor });
                }
            });

            realtimeSensoresChart.update();
        }
    });
});
