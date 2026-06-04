import { t, setLanguage } from "./i18n.js";

const API = "/api/v1";
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

let state = { page: "dashboard", theme: localStorage.getItem("frk-theme") || "light", lang: localStorage.getItem("frk-lang") || "en", crops: [], intercropping: [], corridors: [] };
let charts = {};
let leafletMap = null;

function toast(msg, type = "success") {
  const c = $("#toast");
  const colors = { success: "rgba(27,94,32,.95)", error: "rgba(198,40,40,.95)", info: "rgba(21,101,192,.95)" };
  const icons = { success: "✓", error: "✗", info: "ℹ" };
  const e = document.createElement("div");
  e.className = "ani-in";
  e.style.cssText = `background:${colors[type]||colors.info};color:#fff;padding:.75rem 1.25rem;border-radius:12px;font-size:.8rem;display:flex;align-items:center;gap:.5rem;box-shadow:0 8px 32px rgba(0,0,0,.15);backdrop-filter:blur(12px)`;
  e.innerHTML = `<span style="font-weight:700">${icons[type]||icons.info}</span><span>${msg}</span>`;
  c.appendChild(e);
  setTimeout(() => { e.style.transition = "all .3s"; e.style.opacity = "0"; e.style.transform = "translateY(-10px)"; setTimeout(() => e.remove(), 300); }, 3500);
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
  $("#theme-toggle").textContent = t === "dark" ? "☀️ Light" : "🌙 Dark";
}

function applyLang(l) {
  state.lang = l;
  setLanguage(l);
  localStorage.setItem("frk-lang", l);
  $("#lang-toggle").textContent = `🌐 ${l === "en" ? "Kiswahili" : "English"}`;
}

function destroyChart(key) { if (charts[key]) { charts[key].destroy(); delete charts[key]; } }

function skeleton(count) {
  return Array.from({length:count}, (_,i) => `<div class="skeleton h-${i===0?32:20} w-full"></div>`).join("");
}

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

  // Resilience chart
  destroyChart("resilience");
  const rsCrops = crops.filter(c => c.resilience_score != null).sort((a, b) => a.resilience_score - b.resilience_score);
  const ctx1 = document.getElementById("chart-resilience");
  if (ctx1 && rsCrops.length) {
    const colors = rsCrops.map(c => c.resilience_score > 0.8 ? "rgba(27,94,32,.8)" : c.resilience_score > 0.6 ? "rgba(199,149,43,.8)" : "rgba(229,57,53,.7)");
    charts.resilience = new Chart(ctx1, {
      type: "bar", data: {
        labels: rsCrops.map(c => c.name_en?.split(",")[0]?.trim() || c.key),
        datasets: [{ label: "Resilience (Rs)", data: rsCrops.map(c => c.resilience_score), backgroundColor: colors, borderRadius: 6, borderSkipped: false }]
      }, options: {
        responsive: true, maintainAspectRatio: false, indexAxis: "y",
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: r => `Rs ${r.parsed.x.toFixed(2)}` } } },
        scales: { x: { min: 0, max: 1, ticks: { stepSize: 0.2, font: { size: 10 } }, grid: { display: false } },
                 y: { ticks: { font: { size: 9 } }, grid: { display: false } } }
      }
    });
  }

  // Iron chart
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
          labels, datasets: [{ label: "Iron (mg/kg DW)", data: feValues, backgroundColor: ["rgba(198,40,40,.8)","rgba(229,57,53,.75)","rgba(239,83,80,.7)","rgba(255,112,67,.65)","rgba(255,171,145,.6)","rgba(255,205,210,.5)"], borderRadius: 6, borderSkipped: false }]
        }, options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: { callbacks: { label: r => `${r.parsed.y} mg/kg` } } },
          scales: { y: { beginAtZero: true, ticks: { font: { size: 10 } }, grid: { color: "rgba(0,0,0,.05)" } },
                   x: { ticks: { font: { size: 9 } }, grid: { display: false } } }
        }
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

  const counties = [...new Set(state.crops.flatMap(c => c.counties || []))].sort();
  const sel = document.getElementById("tf-county");
  if (sel && !sel.options.length) { const o = document.createElement("option"); o.value = ""; o.textContent = "Select county..."; sel.appendChild(o); counties.forEach(c => { const o = document.createElement("option"); o.value = c; o.textContent = c; sel.appendChild(o); }); }

  $("#tf-classify-btn")?.addEventListener("click", async () => {
    const input = $("#tf-input");
    const crop = input?.value.trim().toLowerCase();
    if (!crop) return;
    const resp = await api(`/traditional-foods/classify/${encodeURIComponent(crop)}`);
    const el = $("#tf-result");
    if (!el) return;
    el.classList.remove("hidden");
    if (!resp?.classified) {
      el.innerHTML = `<div style="background:rgba(255,193,7,.1);border:1px solid rgba(255,193,7,.2);border-radius:12px;padding:1rem;font-size:.85rem"><p style="font-weight:600">"${crop}" not found</p><p style="color:rgba(0,0,0,.4);font-size:.75rem;margin-top:4px">Try: amaranth, managu, sagaa, mrenda, slenderleaf, mitoo, terere, kunde</p></div>`;
      return;
    }
    const c = resp;
    const sc = c.status === "indigenous" ? "rgba(27,94,32,.12)" : c.status === "naturalised" ? "rgba(21,101,192,.12)" : "rgba(199,149,43,.12)";
    const sc2 = c.status === "indigenous" ? "#1B5E20" : c.status === "naturalised" ? "#1565C0" : "#8B6914";
    el.innerHTML = `<div style="border:1px solid ${sc2}22;border-radius:12px;padding:1rem;background:${sc};font-size:.85rem">
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px">
        <span style="background:${sc2};color:#fff;padding:2px 10px;border-radius:20px;font-size:.65rem;font-weight:600;text-transform:uppercase">${c.status}</span>
        <span style="font-weight:600">${c.name_en || crop}</span>
        <span style="color:rgba(0,0,0,.35);font-size:.75rem">${c.name_sw || ""}</span>
        ${c.resilience_score != null ? `<span style="background:${c.resilience_score>0.8?'rgba(27,94,32,.12)':'rgba(199,149,43,.12)'};color:${c.resilience_score>0.8?'#1B5E20':'#8B6914'};padding:2px 10px;border-radius:20px;font-size:.65rem;font-weight:600">Rs ${c.resilience_score.toFixed(2)}</span>` : ""}
      </div>
      ${c.origin||c.growing_season?`<p style="color:rgba(0,0,0,.45);font-size:.75rem"><strong>Origin:</strong> ${c.origin||"Unknown"} ${c.growing_season?`· <strong>Growing:</strong> ${c.growing_season}`:""}</p>`:""}
      ${c.traditional_uses?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Uses:</strong> ${c.traditional_uses}</p>`:""}
      ${c.nutrition?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Nutrition:</strong> ${c.nutrition}</p>`:""}
      ${c.market_price_kes_tonne?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Market Price:</strong> KES ${Number(c.market_price_kes_tonne).toLocaleString()}/t</p>`:""}
      ${c.intercropping?.length?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Intercrops:</strong> ${c.intercropping.map(i=>i.charAt(0).toUpperCase()+i.slice(1)).join(", ")}</p>`:""}
      ${c.counties?.length?`<p style="color:rgba(0,0,0,.45);font-size:.75rem;margin-top:4px"><strong>Counties:</strong> ${c.counties.join(", ")}</p>`:""}
    </div>`;
  });

  $("#tf-region-btn")?.addEventListener("click", async () => {
    const county = $("#tf-county")?.value;
    if (!county) return;
    const resp = await api(`/traditional-foods/region/${encodeURIComponent(county)}`);
    const el = $("#tf-region-result");
    if (!el) return;
    el.classList.remove("hidden");
    if (!resp || !resp.crop_count) { el.innerHTML = `<div style="background:rgba(255,193,7,.1);border:1px solid rgba(255,193,7,.2);border-radius:12px;padding:1rem;font-size:.85rem">No data for ${county}</div>`; return; }
    el.innerHTML = `<div style="background:rgba(27,94,32,.06);border:1px solid rgba(27,94,32,.15);border-radius:12px;padding:1rem">
      <p style="font-size:.85rem;font-weight:600;margin-bottom:8px">${resp.crop_count} crops in ${county}</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px">${resp.crops.map(c => {
        const sc = c.status === "indigenous" ? "#1B5E20" : c.status === "naturalised" ? "#1565C0" : "#8B6914";
        return `<div style="background:rgba(255,255,255,.6);border-radius:10px;padding:8px;border:1px solid rgba(0,0,0,.04);font-size:.75rem">
          <span style="display:block;font-weight:600">${c.name_en}</span><span style="display:block;color:rgba(0,0,0,.35)">${c.name_sw}</span>
          <span style="color:${sc};font-size:.65rem;font-weight:600">${c.status}</span>
        </div>`;
      }).join("")}</div></div>`;
  });

  const tbody = document.getElementById("tf-table-body");
  if (tbody && state.crops.length) {
    tbody.innerHTML = state.crops.map(c => {
      const sc = c.status === "indigenous" ? "rgba(27,94,32,.12)" : c.status === "naturalised" ? "rgba(21,101,192,.12)" : "rgba(199,149,43,.12)";
      const sc2 = c.status === "indigenous" ? "#1B5E20" : c.status === "naturalised" ? "#1565C0" : "#8B6914";
      const rs = c.resilience_score;
      return `<tr style="border-bottom:1px solid rgba(0,0,0,.04);transition:background .2s" onmouseover="this.style.background='rgba(0,0,0,.02)'" onmouseout="this.style.background=''">
        <td style="padding:10px 8px 10px 12px;font-weight:500;font-size:.8rem">${c.name_en?.split(",")[0]?.trim() || c.key}</td>
        <td style="padding:10px 8px;color:rgba(0,0,0,.35);font-size:.75rem">${c.name_sw || ""}</td>
        <td style="padding:10px 8px"><span style="background:${sc};color:${sc2};padding:2px 10px;border-radius:20px;font-size:.6rem;font-weight:600;text-transform:uppercase">${c.status}</span></td>
        <td style="padding:10px 8px;font-weight:600;font-size:.85rem;color:${rs>0.8?'#1B5E20':rs>0.6?'#8B6914':'#C62828'}">${rs != null ? rs.toFixed(2) : "—"}</td>
        <td style="padding:10px 8px;color:rgba(0,0,0,.4);font-size:.75rem" class="hidden md:table-cell">${c.growing_season || ""}</td>
        <td style="padding:10px 12px 10px 8px;color:rgba(0,0,0,.35);font-size:.65rem" class="hidden lg:table-cell">${c.counties?.slice(0, 3).join(", ") || ""}</td>
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

  const mapEl = document.getElementById("map");
  if (mapEl && !leafletMap) {
    leafletMap = L.map("map", { zoomControl: true, attributionControl: false }).setView([-0.5, 36.8], 6);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 10 }).addTo(leafletMap);
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
      allCities.forEach(l => { bounds.push(locations[l]); L.circleMarker(locations[l], { radius: 6, color: "#1B5E20", fillColor: "#1B5E20", fillOpacity: 0.8, weight: 2 }).addTo(leafletMap).bindPopup(`<b>${l}</b>`); });
      if (allCities.length >= 2) {
        const pts = allCities.map(l => locations[l]).filter(Boolean);
        if (pts.length >= 2) L.polyline(pts, { color: "#C7952B", weight: 2.5, opacity: 0.7, dashArray: "8, 6" }).addTo(leafletMap);
      }
    });
    if (bounds.length) leafletMap.fitBounds(L.latLngBounds(bounds), { padding: [30, 30] });
  }

  const el = document.getElementById("corridor-cards");
  if (el && corridors.length) {
    const icons = ["🌾", "🌿", "🌴", "🍌", "🚛", "🛵", "🚌", "🐪", "🚢"];
    el.innerHTML = corridors.map((c, i) => `<div class="card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px"><span style="font-size:1.2rem">${icons[i % icons.length]}</span><span style="font-weight:600;font-size:.9rem">${c.name}</span></div>
      <p style="font-size:.75rem;color:rgba(0,0,0,.4);margin-bottom:4px">${(c.origin_cities || []).join(", ")} → ${c.destination}</p>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:4px"><strong>Crops:</strong> ${(c.key_crops || []).join(", ")}</p>
      ${c.transport?`<p style="font-size:.7rem;color:rgba(0,0,0,.35);margin-bottom:4px">${c.transport}</p>`:""}
      ${c.food_remittance_context?`<p style="font-size:.7rem;color:var(--teal);margin-bottom:4px">${c.food_remittance_context}</p>`:""}
      ${c.demand_intensity === "very_high" ? '<span class="badge badge-green">High volume</span>' : `<span class="badge badge-gold">${c.demand_intensity}</span>`}
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

  const counties = [...new Set(state.crops.flatMap(c => c.counties || []))].sort();
  $$("select[name='county'], #mp-county-filter").forEach(s => {
    if (s.options.length <= 1) { const o = document.createElement("option"); o.value = ""; o.textContent = "All counties"; s.appendChild(o); counties.forEach(c => { const o = document.createElement("option"); o.value = c; o.textContent = c; s.appendChild(o); }); }
  });

  function renderListings(items) {
    const el = document.getElementById("mp-listings");
    if (!el) return;
    if (!items.length) { el.innerHTML = `<div style="text-align:center;color:rgba(0,0,0,.3);padding:3rem 1rem;font-size:.9rem">No listings. Be the first to post!</div>`; return; }
    el.innerHTML = items.map(l => {
      const sb = l.status === "indigenous" ? "#1B5E20" : l.status === "naturalised" ? "#1565C0" : "#8B6914";
      return `<div class="card" ${l.is_chama?'style=border-left:4px solid var(--gold)':''}>
        <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px">
          <span style="font-weight:600;font-size:.85rem">${l.food}</span>
          <div style="display:flex;gap:4px;flex-wrap:wrap">
            ${l.status?`<span class="badge" style="background:${sb}18;color:${sb}">${l.status}</span>`:""}
            ${l.is_chama?`<span class="badge" style="background:rgba(199,149,43,.12);color:#8B6914">👩‍👩‍👧‍👧 ${l.chama_name||"Chama"}</span>`:""}
          </div>
        </div>
        ${l.food_sw?`<p style="font-size:.75rem;color:rgba(0,0,0,.35);margin-bottom:2px">${l.food_sw}</p>`:""}
        <p style="font-size:1.3rem;font-weight:700;color:var(--green);margin-bottom:2px">KES ${Number(l.price_kes_per_kg).toLocaleString()}/kg</p>
        <p style="font-size:.75rem;color:rgba(0,0,0,.4);margin-bottom:2px">${Number(l.quantity_kg).toLocaleString()} kg · KES ${(l.quantity_kg * l.price_kes_per_kg).toLocaleString()} total</p>
        <p style="font-size:.75rem;color:rgba(0,0,0,.4);margin-bottom:2px">📍 ${l.county} ${l.corridor?`· ${l.corridor}`:""} ${l.delivery_available?'· 🚚 Delivery':""}</p>
        <p style="font-size:.7rem;color:rgba(0,0,0,.3)">${l.seller} ${l.contact?`· ${l.contact}`:""} ${l.created_at?`· ${new Date(l.created_at).toLocaleDateString()}`:""}</p>
      </div>`;
    }).join("");
  }

  renderListings(listings);

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
    e.target.style.background = chamaOn ? "#1B5E20" : "";
    e.target.style.color = chamaOn ? "white" : "";
    renderListings(chamaOn ? listings.filter(l => l.is_chama) : listings);
  });

  $("#mp-de-risk-btn")?.addEventListener("click", () => {
    const c = $("#mp-county-filter")?.value;
    nav("de-risk");
    if (c) setTimeout(() => { const el = document.getElementById("dr-parametrics"); if (el) el.scrollIntoView({ behavior: "smooth" }); }, 200);
  });

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

  const pe = document.getElementById("mp-prices");
  if (pe && Object.keys(prices).length) {
    pe.innerHTML = `<table style="width:100%;font-size:.8rem"><thead><tr style="text-align:left;color:rgba(0,0,0,.4);border-bottom:1px solid rgba(0,0,0,.06)">
      <th style="padding:8px 8px 8px 0;font-weight:500">Crop</th><th style="padding:8px 8px;font-weight:500">KES/t</th><th style="padding:8px 8px;font-weight:500" class="hidden sm:table-cell">30d High</th><th style="padding:8px 8px;font-weight:500">Trend</th><th style="padding:8px 0;font-weight:500">Status</th>
    </tr></thead><tbody>
      ${Object.entries(prices).map(([k, v]) => `<tr style="border-bottom:1px solid rgba(0,0,0,.04)">
        <td style="padding:8px 8px 8px 0;font-size:.75rem">${v.name_en || k}</td>
        <td style="padding:8px 8px;font-weight:600">${Number(v.current).toLocaleString()}</td>
        <td style="padding:8px 8px;color:rgba(0,0,0,.35);font-size:.75rem" class="hidden sm:table-cell">${Number(v.high_30d || 0).toLocaleString()}</td>
        <td style="padding:8px 8px">${v.trend === "up" ? "📈" : v.trend === "down" ? "📉" : "➡️"}</td>
        <td style="padding:8px 0;font-size:.75rem">${v.status === "indigenous" ? "🌿" : v.status === "naturalised" ? "🌱" : "🌾"}</td>
      </tr>`).join("")}
    </tbody></table>`;
  }

  // Markup chart
  destroyChart("markup");
  const mc = document.getElementById("chart-markup");
  if (mc) {
    const retailData = { "Nightshade": 127, "Amaranth": 130, "Cowpea": 143, "Spider Plant": 57, "Pumpkin": 40 };
    charts.markup = new Chart(mc, {
      type: "bar", data: {
        labels: Object.keys(retailData),
        datasets: [
          { label: "Retail Markup %", data: Object.values(retailData), backgroundColor: ["rgba(27,94,32,.8)","rgba(199,149,43,.8)","rgba(198,40,40,.7)","rgba(21,101,192,.7)","rgba(93,64,55,.7)"], borderRadius: 6, borderSkipped: false },
          { label: "PHL Rate (57%)", data: [57, 57, 57, 57, 57], type: "line", borderColor: "#C62828", borderWidth: 2, pointRadius: 0, fill: false, borderDash: [6, 3] }
        ]
      }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "top", labels: { boxWidth: 12, font: { size: 9 } } } }, scales: { y: { beginAtZero: true, grid: { color: "rgba(0,0,0,.04)" } }, x: { grid: { display: false } } } }
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

  const ov = document.getElementById("dr-overview");
  if (ov && overview?.forces) {
    const icons = ["🔥", "💰", "💡", "📚"];
    ov.innerHTML = overview.forces.map((f, i) => `<div class="card" style="border-left:3px solid var(--green)">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px"><span style="font-size:1.1rem">${icons[i]}</span><span style="font-weight:700;font-size:.85rem">${f.name}</span></div>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);line-height:1.5">${f.detail}</p>
      <p style="font-size:.65rem;color:rgba(0,0,0,.25);margin-top:6px">Sources: ${(f.data_sources || []).join(", ")}</p>
    </div>`).join("");
  }

  const pm = document.getElementById("dr-parametrics");
  if (pm && parametrics?.model) {
    const m = parametrics.model;
    pm.innerHTML = `<p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:8px">${m.description}</p>
      <div style="display:flex;flex-direction:column;gap:6px">${(m.trigger_metrics || []).map(t => `
        <div style="background:rgba(0,0,0,.03);border-radius:10px;padding:10px;font-size:.75rem">
          <p style="font-weight:600;margin-bottom:2px;text-transform:capitalize">${t.name.replace(/_/g, " ")}</p>
          <p style="color:rgba(0,0,0,.4);font-size:.7rem">Sensor: ${t.sensor} · Payout: ${t.payout_formula}</p>
          <p style="color:rgba(0,0,0,.35);font-size:.7rem">Threshold: ${t.threshold}</p>
        </div>`
      ).join("")}</div>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-top:8px"><strong>Premium:</strong> ${m.premium_estimate_kes_per_ha}</p>
      ${parametrics.county_context?.primary_risk ? `<p style="font-size:.7rem;color:var(--teal);margin-top:4px">${parametrics.county_context.primary_risk}</p>` : ""}`;
  }

  destroyChart("greenbond");
  const gc = document.getElementById("chart-greenbond");
  if (gc && greenbond?.allocations) {
    charts.greenbond = new Chart(gc, {
      type: "doughnut", data: {
        labels: greenbond.allocations.map(a => a.program),
        datasets: [{ data: greenbond.allocations.map(a => a.allocation_pct), backgroundColor: ["#1B5E20","#C7952B","#00695C","#5D4037"], borderWidth: 0 }]
      }, options: { responsive: true, maintainAspectRatio: false, cutout: "65%", plugins: { legend: { position: "bottom", labels: { boxWidth: 10, font: { size: 9 }, padding: 8 } }, tooltip: { callbacks: { label: r => `${r.label}: ${r.parsed}%` } } } }
    });
  }

  const ue = document.getElementById("dr-usaid");
  if (ue && usaid?.key_metrics) {
    const km = usaid.key_metrics;
    ue.innerHTML = `<p style="font-size:.85rem;font-weight:600;margin-bottom:4px">${km.bilateral_aid_contraction_usd} contraction</p>
      <p style="color:rgba(0,0,0,.45)"><strong>Awards terminated:</strong> ${km.award_termination_rate_pct}</p>
      <p style="color:rgba(0,0,0,.45);margin-top:2px"><strong>CSA mainstreamed:</strong> ${km.csa_mainstreamed_in_counties_pct}% counties</p>
      <p style="color:rgba(0,0,0,.45);margin-top:2px"><strong>CSA funded:</strong> ${km.csa_budget_allocated_pct}%</p>
      <p style="color:rgba(0,0,0,.45);margin-top:2px"><strong>Food insecure:</strong> ${km.food_insecurity_estimate_2026}</p>
      <p style="color:rgba(0,0,0,.3);font-size:.7rem;margin-top:6px">${usaid.systemic_consequence?.slice(0, 120)}...</p>`;
  }

  const ph = document.getElementById("dr-phl");
  if (ph && phl) {
    ph.innerHTML = `<p style="font-size:1.5rem;font-weight:700;color:var(--green);margin-bottom:2px">${phl.aiv_phl_rate_pct}%</p>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:4px">Post-harvest loss rate for AIVs</p>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:8px">Farmer burden <strong>${phl.economic_burden_ratio_farmer_vs_retailer}x</strong> vs retailer</p>
      <div style="display:flex;flex-direction:column;gap:4px">${(phl.interventions || []).map(i => `<div style="background:rgba(0,0,0,.03);border-radius:8px;padding:8px;font-size:.75rem"><p style="font-weight:600;margin-bottom:2px">${i.solution}</p><p style="color:rgba(0,0,0,.4)">Reduces PHL ${i.phl_reduction_pct}%</p></div>`).join("")}</div>`;
  }

  const ce = document.getElementById("dr-carbon");
  if (ce && carbon) {
    const seq = carbon.estimated_sequestration_tonnes_co2_per_ha || {};
    ce.innerHTML = `<p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-bottom:6px">${carbon.description?.slice(0, 120)}</p>
      ${Object.entries(seq).map(([k, v]) => `<div style="display:flex;justify-content:space-between;font-size:.75rem;padding:4px 0;border-bottom:1px solid rgba(0,0,0,.04)"><span style="text-transform:capitalize">${k.replace(/_/g, " ")}</span><span style="font-weight:600;color:${v>0?'var(--green)':'#C62828'}">${v} tCO₂/ha</span></div>`).join("")}
      <p style="font-size:.75rem;color:rgba(0,0,0,.45);margin-top:6px"><strong>Price:</strong> ${carbon.carbon_price_kes_per_tonne}</p>
      <p style="font-size:.75rem;color:rgba(0,0,0,.45)"><strong>Revenue:</strong> ${carbon.additional_revenue_kes_per_ha}/ha</p>`;
  }
}

// ==============================
// INIT
// ==============================
document.addEventListener("DOMContentLoaded", async () => {
  applyLang(state.lang);
  theme(state.theme);

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
