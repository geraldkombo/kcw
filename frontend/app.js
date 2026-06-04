import { t, setLanguage } from "./i18n.js";

const API = "/api/v1";
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

let state = { page: "dashboard", theme: localStorage.getItem("frk-theme") || "light", lang: localStorage.getItem("frk-lang") || "en", crops: [], intercropping: [], corridors: [] };
let charts = {};
let leafletMap = null;

function toast(msg, type = "success") {
  const c = $("#toast");
  const e = document.createElement("div");
  e.className = `${type === "success" ? "bg-green-600" : type === "error" ? "bg-red-600" : "bg-blue-600"} text-white px-4 py-3 rounded-lg shadow-lg text-sm flex items-center gap-2 ani-in`;
  e.innerHTML = `<span>${type === "success" ? "✅" : type === "error" ? "❌" : "ℹ️"}</span><span>${msg}</span>`;
  c.appendChild(e);
  setTimeout(() => { e.classList.add("ani-out"); setTimeout(() => e.remove(), 300); }, 4000);
}

async function api(path, opts = {}) {
  try {
    const r = await fetch(`${API}${path}`, { signal: AbortSignal.timeout(8000), ...opts, headers: { "Content-Type": "application/json", ...opts.headers } });
    if (!r.ok) throw new Error(String(r.status));
    return await r.json();
  } catch { return null; }
}

function nav(page) {
  state.page = page;
  $$("[data-page]").forEach(e => e.classList.add("hidden"));
  const t = $(`[data-page="${page}"]`);
  if (t) t.classList.remove("hidden");
  $$(".nav-link").forEach(l => l.classList.toggle("active", l.dataset.nav === page));
  $$(".bottom-nav-link").forEach(l => l.classList.toggle("active", l.dataset.nav === page));
}

function theme(t) {
  state.theme = t;
  document.documentElement.classList.toggle("dark", t === "dark");
  localStorage.setItem("frk-theme", t);
  const b = $("#theme-toggle");
  if (b) b.innerHTML = t === "dark" ? "☀️ Light" : "🌙 Dark";
}

function applyLang(l) {
  state.lang = l;
  setLanguage(l);
  localStorage.setItem("frk-lang", l);
  $("#lang-label").textContent = l === "en" ? "EN" : "SW";
  const b = $("#lang-toggle");
  if (b) b.innerHTML = `🌐 ${l === "en" ? "Kiswahili" : "English"}`;
}

function destroyChart(key) { if (charts[key]) { charts[key].destroy(); delete charts[key]; } }

// ==============================
// DASHBOARD
// ==============================
async function renderDashboard() {
  const [listResp, corridorResp] = await Promise.all([api("/traditional-foods/list"), api("/traditional-foods/corridors")]);
  const crops = listResp?.crops || state.crops || [];
  state.crops = crops;
  const corr = corridorResp?.corridors || state.corridors || [];
  state.corridors = corr;
  const indigenous = crops.filter(c => c.status === "indigenous").length;

  $("#stat-crops").textContent = crops.length || "—";
  $("#stat-indigenous").textContent = indigenous || "—";
  $("#stat-corridors").textContent = corr.length || "—";
  $("#stat-tests").textContent = "150";

  // Resilience bar chart
  destroyChart("resilience");
  const rsCrops = crops.filter(c => c.resilience_score != null).sort((a, b) => a.resilience_score - b.resilience_score);
  const ctx1 = document.getElementById("chart-resilience");
  if (ctx1 && rsCrops.length) {
    charts.resilience = new Chart(ctx1, {
      type: "bar", data: {
        labels: rsCrops.map(c => c.name_en?.split(",")[0]?.trim() || c.key),
        datasets: [{ label: "Resilience Score (Rs)", data: rsCrops.map(c => c.resilience_score), backgroundColor: rsCrops.map(c => c.resilience_score > 0.8 ? "#2E7D32" : c.resilience_score > 0.6 ? "#FFB300" : "#E53935"), borderRadius: 4 }]
      }, options: { responsive: true, maintainAspectRatio: false, indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { min: 0, max: 1, ticks: { stepSize: 0.2 } } } }
    });
  }

  // Iron bar chart
  destroyChart("iron");
  const ironCtx = document.getElementById("chart-iron");
  if (ironCtx) {
    const mineralData = await Promise.all(
      ["slenderleaf", "black_nightshade", "spider_plant", "jute_mallow", "amaranth", "cowpea_leaves"]
        .map(async c => { const r = await api(`/traditional-foods/nutrition/${c}/minerals`); return r?.mineral_composition_mg_per_kg_dw; })
    );
    const labels = ["Slenderleaf", "Nightshade", "Spider Plant", "Jute Mallow", "Amaranth", "Cowpea"];
    const feValues = mineralData.map(m => m?.Fe || 0);
    if (feValues.some(v => v > 0)) {
      charts.iron = new Chart(ironCtx, {
        type: "bar", data: {
          labels, datasets: [{ label: "Iron (mg/kg DW)", data: feValues, backgroundColor: ["#C62828", "#E53935", "#EF5350", "#FF7043", "#FFAB91", "#FFCDD2"], borderRadius: 4 }]
        }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
      });
    }
  }
}

// ==============================
// TRADITIONAL FOODS
// ==============================
async function renderTraditionalFoods() {
  const crops = state.crops;
  if (!crops.length) { const r = await api("/traditional-foods/list"); state.crops = r?.crops || []; }

  // County dropdown
  const counties = [...new Set(state.crops.flatMap(c => c.counties || []))].sort();
  const sel = document.getElementById("tf-county");
  if (sel && !sel.options.length) counties.forEach(c => { const o = document.createElement("option"); o.value = c; o.textContent = c; sel.appendChild(o); });

  // Classify
  $("#tf-classify-btn")?.addEventListener("click", async () => {
    const input = $("#tf-input");
    const crop = input?.value.trim().toLowerCase();
    if (!crop) return;
    const resp = await api(`/traditional-foods/classify/${encodeURIComponent(crop)}`);
    const el = $("#tf-result");
    if (!el) return;
    el.classList.remove("hidden");
    if (!resp?.classified) {
      el.innerHTML = `<div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 rounded-lg p-3 text-sm"><p class="font-medium">"${crop}" not found</p><p class="text-xs text-gray-500 mt-1">Try: amaranth, managu, sagaa, mrenda, slenderleaf, mitoo, terere, kunde</p></div>`;
      return;
    }
    const c = resp;
    const sc = c.status === "indigenous" ? "green" : c.status === "naturalised" ? "blue" : "gold";
    el.innerHTML = `<div class="bg-${sc}-50 dark:bg-${sc}-900/20 border border-${sc}-200 dark:border-${sc}-800 rounded-lg p-3 space-y-2 text-sm">
      <div class="flex items-center gap-2 flex-wrap">
        <span class="badge badge-${sc}">${c.status}</span>
        <span class="font-medium">${c.name_en || crop}</span>
        <span class="text-xs text-gray-400">${c.name_sw || ""}</span>
        ${c.resilience_score != null ? `<span class="badge badge-${c.resilience_score > 0.8 ? 'green' : c.resilience_score > 0.6 ? 'gold' : 'red'}">Rs ${c.resilience_score.toFixed(2)}</span>` : ""}
      </div>
      <p class="text-xs text-gray-500"><strong>Origin:</strong> ${c.origin || "Unknown"} · <strong>Growing:</strong> ${c.growing_season || ""}</p>
      <p class="text-xs text-gray-500"><strong>Uses:</strong> ${c.traditional_uses || ""}</p>
      ${c.nutrition ? `<p class="text-xs text-gray-500"><strong>Nutrition:</strong> ${c.nutrition}</p>` : ""}
      ${c.market_price_kes_tonne ? `<p class="text-xs text-gray-500"><strong>Market Price:</strong> KES ${Number(c.market_price_kes_tonne).toLocaleString()}/t</p>` : ""}
      ${c.intercropping?.length ? `<p class="text-xs text-gray-500"><strong>Intercrops:</strong> ${c.intercropping.map(i => i.charAt(0).toUpperCase() + i.slice(1)).join(", ")}</p>` : ""}
      ${c.counties?.length ? `<p class="text-xs text-gray-500"><strong>Counties:</strong> ${c.counties.join(", ")}</p>` : ""}
    </div>`;
  });

  // Region search
  $("#tf-region-btn")?.addEventListener("click", async () => {
    const county = $("#tf-county")?.value;
    if (!county) return;
    const resp = await api(`/traditional-foods/region/${encodeURIComponent(county)}`);
    const el = $("#tf-region-result");
    if (!el) return;
    el.classList.remove("hidden");
    if (!resp || !resp.crop_count) { el.innerHTML = `<div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 rounded-lg p-3 text-sm">No data for ${county}</div>`; return; }
    el.innerHTML = `<div class="bg-green-50 dark:bg-green-900/20 border border-green-200 rounded-lg p-3">
      <p class="text-sm font-medium mb-2">${resp.crop_count} crops in ${county}</p>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">${resp.crops.map(c =>
        `<div class="text-xs p-2 bg-white dark:bg-slate-800 rounded border border-green-100 dark:border-green-900">
          <span class="block font-medium">${c.name_en}</span><span class="block text-gray-400">${c.name_sw}</span>
          <span class="badge badge-${c.status === 'indigenous' ? 'green' : c.status === 'naturalised' ? 'blue' : 'gold'} mt-1">${c.status}</span>
        </div>`
      ).join("")}</div></div>`;
  });

  // Crop table
  const tbody = document.getElementById("tf-table-body");
  if (tbody && state.crops.length) {
    tbody.innerHTML = state.crops.map(c => {
      const sc = c.status === "indigenous" ? "green" : c.status === "naturalised" ? "blue" : "gold";
      const rs = c.resilience_score;
      return `<tr class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-slate-700/50">
        <td class="py-2 pr-2 font-medium text-xs">${c.name_en?.split(",")[0]?.trim() || c.key}</td>
        <td class="py-2 pr-2 text-gray-400">${c.name_sw || ""}</td>
        <td class="py-2 pr-2"><span class="badge badge-${sc}">${c.status}</span></td>
        <td class="py-2 pr-2"><span class="${rs > 0.8 ? 'text-frk-green' : rs > 0.6 ? 'text-frk-gold' : 'text-red-500'} font-semibold">${rs != null ? rs.toFixed(2) : "—"}</span></td>
        <td class="py-2 pr-2 hidden md:table-cell text-gray-500">${c.growing_season || ""}</td>
        <td class="py-2 text-gray-500 text-[10px]">${c.counties?.slice(0, 3).join(", ") || ""}</td>
      </tr>`;
    }).join("");
  }
}

// ==============================
// CORRIDORS
// ==============================
async function renderCorridors() {
  let corridors = state.corridors;
  if (!corridors.length) { const r = await api("/traditional-foods/corridors"); corridors = r?.corridors || []; state.corridors = corridors; }

  // Map
  const mapEl = document.getElementById("map");
  if (mapEl && !leafletMap) {
    leafletMap = L.map("map").setView([-0.5, 36.8], 6);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "&copy; OpenStreetMap", maxZoom: 10 }).addTo(leafletMap);
    const bounds = [];
    const locations = {
      "Nairobi": [-1.2921, 36.8219], "Kisumu": [-0.1022, 34.7617], "Mombasa": [-4.0435, 39.6682],
      "Busia": [0.4614, 34.1121], "Namanga": [-2.5431, 36.7884], "Lodwar": [3.1214, 35.6047],
      "Machakos": [-1.5177, 37.2634], "Kitui": [-1.3704, 38.0106], "Makueni": [-1.8049, 37.6207],
      "Homa Bay": [-0.5229, 34.4565], "Siaya": [0.0611, 34.2898], "Migori": [-1.0667, 34.4731],
      "Kakamega": [0.2843, 34.7522], "Bungoma": [0.5714, 34.5584], "Kiambu": [-1.1711, 36.8354],
      "Murang'a": [-0.7226, 37.1537], "Nyeri": [-0.4222, 36.9509], "Meru": [0.0476, 37.6494],
      "Embu": [-0.5378, 37.4593], "Tharaka Nithi": [-0.2833, 37.8667],
      "Arusha": [-3.3869, 36.6830], "Tororo": [0.6950, 34.1800],
      "Nakuru": [-0.3071, 36.0730], "Baringo": [0.4667, 35.9667], "Kajiado": [-1.8500, 36.7833],
      "Narok": [-1.0833, 35.8667], "Kilifi": [-3.6333, 39.8500], "Kwale": [-4.1833, 39.4500],
    };
    corridors.forEach(c => {
      const allCities = [...(c.origin_cities || []), c.destination].flatMap(n => {
        const parts = n.replace(/\(.*?\)/g, "").split(",");
        return parts.map(p => p.trim());
      }).filter(l => locations[l]);
      allCities.forEach(l => { bounds.push(locations[l]); L.circleMarker(locations[l], { radius: 6, color: "#2E7D32", fillColor: "#2E7D32", fillOpacity: 0.8 }).addTo(leafletMap).bindPopup(l); });
      if (allCities.length >= 2) {
        const pts = allCities.map(l => locations[l]).filter(Boolean);
        if (pts.length >= 2) L.polyline(pts, { color: "#FFB300", weight: 2, opacity: 0.6 }).addTo(leafletMap);
      }
    });
    if (bounds.length) leafletMap.fitBounds(L.latLngBounds(bounds), { padding: [30, 30] });
  }

  // Cards
  const el = document.getElementById("corridor-cards");
  if (el && corridors.length) {
    const icons = ["🌾", "🌿", "🌴", "🍌", "🚛", "🛵", "🚌", "🐪", "🚢"];
    el.innerHTML = corridors.map((c, i) => `<div class="card space-y-1">
      <div class="flex items-center gap-2"><span>${icons[i % icons.length]}</span><span class="font-semibold text-sm">${c.name}</span></div>
      <p class="text-xs text-gray-500">${(c.origin_cities || []).join(", ")} → ${c.destination}</p>
      <p class="text-xs text-gray-500"><strong>Crops:</strong> ${(c.key_crops || []).join(", ")}</p>
      ${c.transport ? `<p class="text-xs text-gray-400">${c.transport}</p>` : ""}
      ${c.food_remittance_context ? `<p class="text-xs text-frk-teal">${c.food_remittance_context}</p>` : ""}
      ${c.demand_intensity === "very_high" ? `<span class="badge badge-green">High volume</span>` : `<span class="badge badge-gold">${c.demand_intensity}</span>`}
    </div>`).join("");
  }
}

// ==============================
// MARKETPLACE
// ==============================
async function renderMarketplace() {
  const [listResp, priceResp] = await Promise.all([api("/marketplace/listings"), api("/marketplace/prices")]);
  const listings = listResp?.listings || [];
  const prices = priceResp?.prices || {};

  // County dropdowns
  const counties = [...new Set(state.crops.flatMap(c => c.counties || []))].sort();
  $$("select[name='county'], #mp-county-filter").forEach(s => {
    if (s.options.length <= 1) { counties.forEach(c => { const o = document.createElement("option"); o.value = c; o.textContent = c; s.appendChild(o); }); }
  });

  function renderListings(items) {
    const el = document.getElementById("mp-listings");
    if (!el) return;
    if (!items.length) { el.innerHTML = `<div class="col-span-full text-center text-gray-400 py-8">No listings. Post one!</div>`; return; }
    el.innerHTML = items.map(l => {
      const sb = l.status === "indigenous" ? "green" : l.status === "naturalised" ? "blue" : "gold";
      return `<div class="card space-y-1 ${l.is_chama ? 'border-l-4 border-frk-gold' : ''}">
        <div class="flex items-center justify-between gap-2">
          <span class="font-semibold text-sm">${l.food}</span>
          <div class="flex gap-1 flex-wrap">
            ${l.status ? `<span class="badge badge-${sb}">${l.status}</span>` : ""}
            ${l.is_chama ? `<span class="badge badge-blue">👩‍👩‍👧‍👧 ${l.chama_name || "Chama"}</span>` : ""}
          </div>
        </div>
        ${l.food_sw ? `<p class="text-xs text-gray-400">${l.food_sw}</p>` : ""}
        <p class="text-lg font-bold text-frk-green">KES ${Number(l.price_kes_per_kg).toLocaleString()}/kg</p>
        <p class="text-xs text-gray-500">${Number(l.quantity_kg).toLocaleString()} kg · KES ${(l.quantity_kg * l.price_kes_per_kg).toLocaleString()} total</p>
        <p class="text-xs text-gray-500">📍 ${l.county} ${l.corridor ? `· ${l.corridor}` : ""} ${l.delivery_available ? '· 🚚 Delivery' : ""}</p>
        <p class="text-xs text-gray-400">${l.seller} ${l.contact ? `· ${l.contact}` : ""} · ${l.created_at ? new Date(l.created_at).toLocaleDateString() : ""}</p>
      </div>`;
    }).join("");
  }

  renderListings(listings);

  // Filters
  $("#mp-filter-btn")?.addEventListener("click", () => {
    const search = $("#mp-search")?.value.trim().toLowerCase();
    const county = $("#mp-county-filter")?.value;
    let f = listings;
    if (search) f = f.filter(l => l.food?.toLowerCase().includes(search) || l.food_sw?.toLowerCase().includes(search));
    if (county) f = f.filter(l => l.county === county);
    renderListings(f);
  });

  let chamaOn = false;
  $("#mp-chama-btn")?.addEventListener("click", (e) => {
    chamaOn = !chamaOn;
    e.target.style.background = chamaOn ? "#2E7D32" : "";
    e.target.style.color = chamaOn ? "white" : "";
    renderListings(chamaOn ? listings.filter(l => l.is_chama) : listings);
  });

  $("#mp-de-risk-btn")?.addEventListener("click", () => {
    const c = $("#mp-county-filter")?.value;
    nav("de-risk");
    if (c) setTimeout(() => { const el = document.getElementById("dr-parametrics"); if (el) el.scrollIntoView({ behavior: "smooth" }); }, 200);
  });

  // Post listing
  $("#mp-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd.entries());
    body.is_chama = fd.has("is_chama");
    body.quantity_kg = parseFloat(body.quantity_kg) || 0;
    body.price_kes_per_kg = parseFloat(body.price_kes_per_kg) || 0;
    const resp = await api("/marketplace/listings", { method: "POST", body: JSON.stringify(body) });
    if (resp) { toast("Listing posted!"); e.target.reset(); renderMarketplace(); }
    else toast("Failed to post", "error");
  });

  // Prices table
  const pe = document.getElementById("mp-prices");
  if (pe && Object.keys(prices).length) {
    pe.innerHTML = `<table class="w-full"><thead><tr class="text-left text-gray-500 border-b dark:border-gray-700"><th class="py-1 pr-2">Crop</th><th class="py-1 pr-2">KES/t</th><th class="py-1 pr-2 hidden sm:table-cell">30d High</th><th class="py-1 pr-2">Trend</th><th class="py-1">Status</th></tr></thead><tbody>
      ${Object.entries(prices).map(([k, v]) => `<tr class="border-b border-gray-100 dark:border-gray-800">
        <td class="py-1 pr-2 text-xs">${v.name_en || k}</td>
        <td class="py-1 pr-2 font-medium text-xs">${Number(v.current).toLocaleString()}</td>
        <td class="py-1 pr-2 text-gray-400 text-xs hidden sm:table-cell">${Number(v.high_30d || 0).toLocaleString()}</td>
        <td class="py-1 pr-2 text-xs">${v.trend === "up" ? "📈" : v.trend === "down" ? "📉" : "➡️"}</td>
        <td class="py-1 text-xs">${v.status === "indigenous" ? "🌿" : v.status === "naturalised" ? "🌱" : "🌾"}</td>
      </tr>`).join("")}
    </tbody></table>`;
  }

  // Retail markup chart
  destroyChart("markup");
  const mc = document.getElementById("chart-markup");
  if (mc) {
    const retailData = { "Nightshade": 127, "Amaranth": 130, "Cowpea": 143, "Spider Plant": 57, "Pumpkin": 40 };
    charts.markup = new Chart(mc, {
      type: "bar", data: {
        labels: Object.keys(retailData),
        datasets: [
          { label: "Retail Markup %", data: Object.values(retailData), backgroundColor: ["#2E7D32", "#FFB300", "#C62828", "#1565C0", "#5D4037"], borderRadius: 4 },
          { label: "PHL Rate (57%)", data: [57, 57, 57, 57, 57], type: "line", borderColor: "#E53935", borderWidth: 2, pointRadius: 0, fill: false }
        ]
      }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "top", labels: { boxWidth: 12, font: { size: 10 } } } }, scales: { y: { beginAtZero: true, title: { display: true, text: "%" } } } }
    });
  }
}

// ==============================
// DE-RISK
// ==============================
async function renderDeRisk() {
  const [overview, parametrics, greenbond, usaid, phl, carbon] = await Promise.all([
    api("/de-risk/overview"), api("/de-risk/parametrics"), api("/de-risk/green-bond"),
    api("/de-risk/usaid-impact"), api("/de-risk/post-harvest-loss"), api("/de-risk/carbon-credits"),
  ]);

  // 4 Forces
  const ov = document.getElementById("dr-overview");
  if (ov && overview?.forces) {
    const icons = ["🔥", "💰", "💡", "📚"];
    ov.innerHTML = overview.forces.map((f, i) => `<div class="card border-l-4 border-frk-green space-y-1">
      <div class="flex items-center gap-2"><span class="text-lg">${icons[i]}</span><span class="font-bold text-sm">${f.name}</span></div>
      <p class="text-xs text-gray-500">${f.detail}</p>
      <p class="text-[10px] text-gray-400">Sources: ${(f.data_sources || []).join(", ")}</p>
    </div>`).join("");
  }

  // Parametrics
  const pm = document.getElementById("dr-parametrics");
  if (pm && parametrics?.model) {
    const m = parametrics.model;
    pm.innerHTML = `<p class="text-xs text-gray-500 mb-2">${m.description}</p>
      <div class="space-y-2">${(m.trigger_metrics || []).map(t => `
        <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-2 text-xs"><p class="font-medium">${t.name.replace(/_/g, " ")}</p>
        <p class="text-gray-500">Sensor: ${t.sensor} | Payout: ${t.payout_formula}</p>
        <p class="text-gray-500">Threshold: ${t.threshold}</p></div>`
      ).join("")}</div>
      <p class="text-xs text-gray-500 mt-2"><strong>Premium estimate:</strong> ${m.premium_estimate_kes_per_ha}</p>
      ${parametrics.county_context?.primary_risk ? `<p class="text-xs text-frk-teal mt-1">${parametrics.county_context.primary_risk}</p>` : ""}`;
  }

  // Green Bond donut
  destroyChart("greenbond");
  const gc = document.getElementById("chart-greenbond");
  if (gc && greenbond?.allocations) {
    charts.greenbond = new Chart(gc, {
      type: "doughnut", data: {
        labels: greenbond.allocations.map(a => a.program),
        datasets: [{ data: greenbond.allocations.map(a => a.allocation_pct), backgroundColor: ["#2E7D32", "#FFB300", "#1565C0", "#5D4037"] }]
      }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom", labels: { boxWidth: 10, font: { size: 9 } } } } }
    });
  }

  // USAID
  const ue = document.getElementById("dr-usaid");
  if (ue && usaid?.key_metrics) {
    const km = usaid.key_metrics;
    ue.innerHTML = `<p class="text-xs font-medium">${km.bilateral_aid_contraction_usd} contraction</p>
      <p class="text-xs text-gray-500">Award termination: ${km.award_termination_rate_pct}</p>
      <p class="text-xs text-gray-500">${km.csa_mainstreamed_in_counties_pct}% counties CSA mainstreamed</p>
      <p class="text-xs text-gray-500">Only ${km.csa_budget_allocated_pct}% funded</p>
      <p class="text-xs text-gray-500">Food insecure: ${km.food_insecurity_estimate_2026}</p>
      <p class="text-xs text-gray-400 mt-1">${usaid.systemic_consequence?.slice(0, 120)}...</p>`;
  }

  // PHL
  const ph = document.getElementById("dr-phl");
  if (ph && phl) {
    ph.innerHTML = `<p class="text-lg font-bold text-frk-green">${phl.aiv_phl_rate_pct}%</p>
      <p class="text-xs text-gray-500">Post-harvest loss rate for AIVs</p>
      <p class="text-xs text-gray-500">Farmer burden ${phl.economic_burden_ratio_farmer_vs_retailer}x vs retailer</p>
      <div class="mt-2 space-y-1">${(phl.interventions || []).map(i => `<div class="text-xs bg-gray-50 dark:bg-slate-700 rounded p-2"><p class="font-medium">${i.solution}</p><p class="text-gray-500">Reduces PHL ${i.phl_reduction_pct}%</p></div>`).join("")}</div>`;
  }

  // Carbon
  const ce = document.getElementById("dr-carbon");
  if (ce && carbon) {
    const seq = carbon.estimated_sequestration_tonnes_co2_per_ha || {};
    ce.innerHTML = `<p class="text-xs text-gray-500 mb-1">${carbon.description?.slice(0, 120)}</p>
      ${Object.entries(seq).map(([k, v]) => `<div class="flex justify-between text-xs py-1 border-b border-gray-100 dark:border-gray-700"><span>${k.replace(/_/g, " ")}</span><span class="font-semibold ${v > 0 ? 'text-frk-green' : 'text-red-500'}">${v} tCO₂/ha</span></div>`).join("")}
      <p class="text-xs text-gray-500 mt-2">Price: ${carbon.carbon_price_kes_per_tonne}</p>
      <p class="text-xs text-gray-500">Revenue: ${carbon.additional_revenue_kes_per_ha}/ha</p>`;
  }
}

// ==============================
// INIT
// ==============================
document.addEventListener("DOMContentLoaded", async () => {
  applyLang(state.lang);
  theme(state.theme);

  // Navigation
  $$(".nav-link, .bottom-nav-link").forEach(l => l.addEventListener("click", (e) => {
    e.preventDefault();
    nav(l.dataset.nav);
    const pages = { dashboard: renderDashboard, "traditional-foods": renderTraditionalFoods, corridors: renderCorridors, marketplace: renderMarketplace, "de-risk": renderDeRisk };
    const fn = pages[l.dataset.nav];
    if (fn) setTimeout(fn, 50);
    if (l.dataset.nav === "corridors") setTimeout(() => { if (leafletMap) leafletMap.invalidateSize(); }, 200);
  }));

  $("#theme-toggle")?.addEventListener("click", () => theme(state.theme === "light" ? "dark" : "light"));
  $("#lang-toggle")?.addEventListener("click", () => applyLang(state.lang === "en" ? "sw" : "en"));

  nav("dashboard");
  await renderDashboard();
  renderTraditionalFoods();
});
