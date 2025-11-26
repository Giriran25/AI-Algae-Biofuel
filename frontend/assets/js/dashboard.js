let trendChart, biomassChart;
const phHistory = [];
const tempHistory = [];
const biomassHistory = [];
const labelHistory = [];

// --------------------------------------------
// INIT CHARTS
// --------------------------------------------
function initCharts() {
  const ctx1 = document.getElementById("trendChart").getContext("2d");
  const ctx2 = document.getElementById("biomassChart").getContext("2d");

  trendChart = new Chart(ctx1, {
    type: "line",
    data: {
      labels: labelHistory,
      datasets: [
        {
          label: "pH",
          data: phHistory,
          borderColor: "#128c4a",
          backgroundColor: "rgba(18,140,74,0.15)",
          tension: 0.3,
        },
        {
          label: "Temperature (°C)",
          data: tempHistory,
          borderColor: "#2182ff",
          backgroundColor: "rgba(33,130,255,0.15)",
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      scales: { x: { display: false } },
    },
  });

  biomassChart = new Chart(ctx2, {
    type: "line",
    data: {
      labels: labelHistory,
      datasets: [
        {
          label: "Biomass Prediction",
          data: biomassHistory,
          borderColor: "#0b6c37",
          backgroundColor: "rgba(11,108,55,0.15)",
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      scales: { x: { display: false } },
    },
  });
}

// --------------------------------------------
// READ REALTIME DATA (OR FALLBACK SYNTHETIC)
// --------------------------------------------
async function refreshDashboard() {
  let latest, pred;

  try {
    latest = await apiGet("/latest"); 
    // Expected: {pH, temperature, turbidity}
  } catch (err) {
    console.warn("API /latest missing → using fallback synthetic data…");

    latest = {
      pH: parseFloat((7 + Math.random() * 1).toFixed(2)),
      temperature: parseFloat((24 + Math.random() * 3).toFixed(2)),
      turbidity: parseFloat((20 + Math.random() * 10).toFixed(1)),
      timestamp: new Date().toLocaleTimeString(),
    };
  }

  try {
    pred = await apiPost("/predict", {
      pH: latest.pH,
      temperature: latest.temperature,
      turbidity: latest.turbidity,
    });
  } catch (err) {
    console.warn("API /predict unavailable → using fallback synthetic prediction…");

    pred = {
      biomass_prediction: parseFloat((0.25 + Math.random() * 0.1).toFixed(3)),
    };
  }

  // --------------------------------------------
  // UPDATE UI CARDS
  // --------------------------------------------
  document.getElementById("card-ph").textContent = latest.pH.toFixed(2);
  document.getElementById("card-temp").textContent =
    latest.temperature.toFixed(1) + "°C";
  document.getElementById("card-turb").textContent =
    latest.turbidity.toFixed(1);

  const biomass = pred.biomass_prediction ?? 0;

  const status =
    biomass > 0.40 ? "Excellent" :
    biomass > 0.25 ? "Optimal" :
    "Needs Tuning";

  document.getElementById("card-status").textContent = status;

  // --------------------------------------------
  // UPDATE CHART DATA
  // --------------------------------------------
  const timeLabel = new Date().toLocaleTimeString();

  labelHistory.push(timeLabel);
  phHistory.push(latest.pH);
  tempHistory.push(latest.temperature);
  biomassHistory.push(biomass);

  // Limit to last 20 points
  if (labelHistory.length > 20) {
    labelHistory.shift();
    phHistory.shift();
    tempHistory.shift();
    biomassHistory.shift();
  }

  trendChart.update();
  biomassChart.update();

  // --------------------------------------------
  // UPDATE LAST UPDATE TIMESTAMP
  // --------------------------------------------
  document.getElementById("last-update").textContent =
    "Last update: " + timeLabel;
}

// --------------------------------------------
// INITIALIZE DASHBOARD
// --------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  initCharts();
  refreshDashboard();
  setInterval(refreshDashboard, 5000); // every 5 seconds
});
