// ----------------------------
// Manual Input – JS Controller
// ----------------------------

let historyPh = [];
let historyTemp = [];
let historyTurb = [];
let historyLabels = [];
let manualChart;

// init mini chart
function initManualChart() {
    const ctx = document.getElementById("manualTrend").getContext("2d");

    manualChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: historyLabels,
            datasets: [
                {
                    label: "pH",
                    data: historyPh,
                    borderColor: "#128c4a",
                    tension: 0.3
                },
                {
                    label: "Temp (°C)",
                    data: historyTemp,
                    borderColor: "#2182ff",
                    tension: 0.3
                },
                {
                    label: "Turbidity",
                    data: historyTurb,
                    borderColor: "#9b59b6",
                    tension: 0.3
                }
            ]
        },
        options: {
            plugins: { legend: { display: false }},
            scales: { x: { display: false }}
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initManualChart();
});

// --------------------------------------------
// HANDLE FORM SUBMISSION → CALL API /predict
// --------------------------------------------
document.getElementById("manualForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const ph = parseFloat(document.getElementById("phInput").value);
    const temp = parseFloat(document.getElementById("tempInput").value);
    const turb = parseFloat(document.getElementById("turbInput").value);

    // send to backend
    let response;
    try {
        response = await apiPost("/predict", {
            pH: ph,
            temperature: temp,
            turbidity: turb
        });
    } catch (err) {
        console.error("Prediction API error:", err);
        return;
    }

    // extract predicted biomass
    const biomass = response.biomass_prediction ?? 0;

    // UPDATE UI — this is your prediction
    document.getElementById("manual-biomass").textContent = biomass.toFixed(4);

    // UPDATE SUGGESTIONS
    updateSuggestions(ph, temp, turb);

    // UPDATE CURRENT VS OPTIMAL TABLE
    updateOptimalTable(ph, temp, turb);

    // UPDATE MINI TREND GRAPH
    pushChartValues(ph, temp, turb);
});

// ---------------------------------------------
// UPDATE SUGGESTIONS BASED ON CURRENT INPUTS
// ---------------------------------------------
function updateSuggestions(ph, temp, turb) {
    const sugBox = document.getElementById("manual-suggestions");
    sugBox.innerHTML = "";  // reset

    const suggestions = [];

    // simple suggestion logic
    if (ph < 7) suggestions.push("Increase pH – culture is too acidic.");
    if (ph > 8.5) suggestions.push("Decrease pH – slightly alkaline.");

    if (temp < 22) suggestions.push("Increase temperature for better biomass yield.");
    if (temp > 32) suggestions.push("Temperature too high – cooling recommended.");

    if (turb < 10) suggestions.push("Low turbidity – biomass concentration is low.");
    if (turb > 50) suggestions.push("High turbidity – possible contamination or overgrowth.");

    // fallback if all ok
    if (suggestions.length === 0) {
        suggestions.push("All parameters are within optimal range!");
    }

    // insert into HTML
    suggestions.forEach(s => {
        const li = document.createElement("li");
        li.textContent = s;
        sugBox.appendChild(li);
    });
}

// -------------------------------------------------
// UPDATE "Current vs Optimal" TABLE
// -------------------------------------------------
function updateOptimalTable(ph, temp, turb) {
    const tbody = document.getElementById("current-optimal");

    const OPTIMAL = {
        pH: 8.2,
        temperature: 27.0,
        turbidity: 25.0
    };

    tbody.innerHTML = `
      <tr><td>pH</td><td>${ph.toFixed(2)}</td><td>${OPTIMAL.pH}</td></tr>
      <tr><td>Temperature</td><td>${temp.toFixed(1)}°C</td><td>${OPTIMAL.temperature}°C</td></tr>
      <tr><td>Turbidity</td><td>${turb.toFixed(1)}</td><td>${OPTIMAL.turbidity}</td></tr>
    `;
}

// -------------------------------------------------
// CHART DATA UPDATE
// -------------------------------------------------
function pushChartValues(ph, temp, turb) {
    const timeLabel = new Date().toLocaleTimeString();

    historyLabels.push(timeLabel);
    historyPh.push(ph);
    historyTemp.push(temp);
    historyTurb.push(turb);

    // keep only 8 readings
    if (historyLabels.length > 8) {
        historyLabels.shift();
        historyPh.shift();
        historyTemp.shift();
        historyTurb.shift();
    }

    manualChart.update();
}
