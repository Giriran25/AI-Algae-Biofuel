// frontend/assets/js/algae.js
document.addEventListener("DOMContentLoaded", async () => {
  const grid = document.getElementById("algaeGrid");

  // attempt to load from backend, otherwise use fallback list
  let data;
  try {
    data = await apiGet("/algae-info");
  } catch (err) {
    // fallback dataset (publicly known ranges / common facts)
    data = [
      {
        name: "Chlorella vulgaris",
        lipid_content: "20–30%",
        temp_range: "20–30°C",
        ph_range: "7.0–8.5",
        speed_label: "Moderate",
        characteristics: "High protein, robust freshwater strain; good lipid productivity under N-starvation.",
        img: "https://upload.wikimedia.org/wikipedia/commons/3/36/Chlorella_vulgaris.jpg",
        applications: ["Biodiesel", "Bioethanol", "Animal feed"]
      },
      {
        name: "Nannochloropsis oculata",
        lipid_content: "30–50%",
        temp_range: "20–25°C",
        ph_range: "7.5–9.0",
        speed_label: "Moderate to Fast",
        characteristics: "Marine species with high lipid productivity; often used for biodiesel.",
        applications: ["Biodiesel (primary)", "Bioethanol", "Omega-3 production"]
      },
      {
        name: "Dunaliella salina",
        lipid_content: "14–20%",
        temp_range: "25–30°C",
        ph_range: "7.0–8.0",
        speed_label: "Moderate",
        characteristics: "Halotolerant, high carotenoid content; used in specialty products and biofuel research.",
        applications: ["Biofuel", "Beta-carotene production"]
      },
      {
        name: "Spirulina (Arthrospira)",
        lipid_content: "4–16%",
        temp_range: "32–35°C",
        ph_range: "8.5–10.0",
        speed_label: "Fast",
        characteristics: "High protein, fast growth; often cultivated for food supplements but researched for biofuel feedstock.",
        applications: ["Biofuel", "Nutritional supplements", "Biogas"]
      },
      {
        name: "Scenedesmus obliquus",
        lipid_content: "20–40%",
        temp_range: "20–30°C",
        ph_range: "6.5–8.0",
        speed_label: "Fast",
        characteristics: "Freshwater species, robust growth and good biomass productivity.",
        applications: ["Biodiesel", "Wastewater treatment"]
      }
    ];
  }

  grid.innerHTML = data.map(a => `
    <article class="algae-card">
      <div class="algae-name-row">
        <div>
          <div class="algae-name">${a.name}</div>
          <div class="algae-meta">Lipid Content: ${a.lipid_content}</div>
        </div>
        <span class="badge-pill ${a.speed_label && a.speed_label.toLowerCase().includes('fast') ? 'badge-fast' : 'badge-moderate'}">${a.speed_label || 'Moderate'}</span>
      </div>
      <div class="algae-meta" style="margin-top:6px;">
        🌡 Temp: ${a.temp_range}<br/>
        ⚗️ pH: ${a.ph_range}
      </div>
      <div style="margin-top:8px;">
        <div style="font-weight:600;font-size:0.9rem;">Characteristics</div>
        <div class="algae-meta">${a.characteristics}</div>
      </div>
      <div style="margin-top:8px;">
        <div style="font-weight:600;font-size:0.9rem;">Applications</div>
        <div class="algae-app-tags">
          ${a.applications.map(app => `<span class="tag">${app}</span>`).join("")}
        </div>
      </div>
    </article>
  `).join('');
});
