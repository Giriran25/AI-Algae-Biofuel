// frontend/assets/js/industry.js
document.addEventListener("DOMContentLoaded", async () => {
  let data;
  try {
    data = await apiGet("/industry-usage");
  } catch (err) {
    // fallback sample industry data (public sources summary)
    data = {
      market: {
        size_2024: "7.2", // billion
        size_2030: "12.8",
        cagr: 10.2,
        outlook: "Strong Growth"
      },
      companies: [
        { name: "Algenol", country: "USA", focus: "Direct-to-ethanol from cyanobacteria", production: "Bioethanol, sustainable fuels" },
        { name: "Sapphire Energy", country: "USA", focus: "'Green crude' from algae", production: "Drop-in replacement fuels" },
        { name: "Solazyme (TerraVia)", country: "USA", focus: "Heterotrophic algal oils", production: "Renewable oils, biofuels" },
        { name: "Cellana", country: "USA/Hawaii", focus: "Offshore cultivation systems", production: "Biofuels, animal feed" },
        { name: "Cyanotech", country: "USA/Hawaii", focus: "Spirulina cultivation", production: "Nutritional products, biofeedstock" },
        { name: "Parry Nutraceuticals", country: "India", focus: "Large-scale Spirulina production", production: "Biofuel, nutraceuticals" }
      ]
    };
  }

  // render market overview
  const mv = document.getElementById("marketOverview");
  mv.innerHTML = `
    <div class="grid-4" style="align-items:stretch;">
      <div class="card-soft card-metric">
        <div class="card-metric-label">Market Size 2024</div>
        <div class="card-metric-value">$${data.market.size_2024}</div>
        <div class="card-metric-sub">Billion USD</div>
      </div>
      <div class="card-soft card-metric">
        <div class="card-metric-label">Projected 2030</div>
        <div class="card-metric-value">$${data.market.size_2030}</div>
        <div class="card-metric-sub">Billion USD</div>
      </div>
      <div class="card-soft card-metric">
        <div class="card-metric-label">CAGR</div>
        <div class="card-metric-value">${data.market.cagr}%</div>
        <div class="card-metric-sub">Compound annual growth</div>
      </div>
      <div class="card-soft card-metric">
        <div class="card-metric-label">Growth Outlook</div>
        <div class="card-metric-value">${data.market.outlook}</div>
        <div class="card-metric-sub">Market indicators</div>
      </div>
    </div>`;

  // render companies
  const grid = document.getElementById("industryGrid");
  grid.innerHTML = data.companies.map(c => `
    <article class="algae-card">
      <div class="algae-name-row">
        <div class="algae-name">${c.name}</div>
        <span class="country-pill">${c.country}</span>
      </div>
      <div class="algae-meta" style="margin-top:6px;">
        <b>Focus Area:</b> ${c.focus}<br/>
        <b>Production:</b> ${c.production}
      </div>
    </article>
  `).join('');
});
