// Kilimo Credit Web — Full Application
import { t, setLanguage, currentLang, LANGUAGES } from "./i18n.js";

// ==============================
// Constants
// ==============================
// CHANGE THIS to your Render backend URL when deploying:
//   const API_BASE = "https://kcw-api.onrender.com";
// For local dev behind nginx, keep as "/api/v1":
const API_BASE = "/api/v1";
let USE_MOCK = false;
const THEME_KEY = "kcw-theme";
const LANG_KEY = "kcw-lang";

const MOCK_FARMERS = [
  { id: "KCW-001", first_name: "Grace", last_name: "Wanjiku", county: "Kiambu", primary_crop: "maize", farm_size_ha: 2.5, credit_score: 68.5, probability_default: 0.12, gender: "F", status: "active", chama_member: true, sacco_member: true, phone: "+254712345001", lat: -1.0092, lng: 36.899 },
  { id: "KCW-002", first_name: "Peter", last_name: "Kiprop", county: "Nakuru", primary_crop: "maize", farm_size_ha: 4.0, credit_score: 45.0, probability_default: 0.33, gender: "M", status: "active", chama_member: false, sacco_member: false, phone: "+254712345002", lat: -0.2919, lng: 35.952 },
  { id: "KCW-003", first_name: "Achieng", last_name: "Odhiambo", county: "Kisumu", primary_crop: "kale", farm_size_ha: 1.2, credit_score: 72.0, probability_default: 0.08, gender: "F", status: "active", chama_member: true, sacco_member: false, phone: "+254712345003", lat: -0.175, lng: 34.917 },
  { id: "KCW-004", first_name: "Mwangi", last_name: "Kimani", county: "Meru", primary_crop: "coffee", farm_size_ha: 3.0, credit_score: 81.0, probability_default: 0.05, gender: "M", status: "active", chama_member: false, sacco_member: true, phone: "+254712345004", lat: 0.05, lng: 37.65 },
  { id: "KCW-005", first_name: "Mary", last_name: "Mutua", county: "Machakos", primary_crop: "beans", farm_size_ha: 2.0, credit_score: 55.0, probability_default: 0.22, gender: "F", status: "active", chama_member: true, sacco_member: false, phone: "+254712345005", lat: -1.517, lng: 37.333 },
  { id: "KCW-006", first_name: "Jane", last_name: "Chebet", county: "Uasin Gishu", primary_crop: "maize", farm_size_ha: 5.0, credit_score: 76.5, probability_default: 0.09, gender: "F", status: "active", chama_member: true, sacco_member: true, phone: "+254712345006", lat: 0.516, lng: 35.28 },
  { id: "KCW-007", first_name: "Benard", last_name: "Ochieng", county: "Homa Bay", primary_crop: "banana", farm_size_ha: 1.5, credit_score: 38.0, probability_default: 0.42, gender: "M", status: "active", chama_member: true, sacco_member: false, phone: "+254712345007", lat: -0.367, lng: 34.65 },
  { id: "KCW-008", first_name: "Sarah", last_name: "Wekesa", county: "Bungoma", primary_crop: "sugarcane", farm_size_ha: 2.8, credit_score: 61.0, probability_default: 0.17, gender: "F", status: "active", chama_member: true, sacco_member: true, phone: "+254712345008", lat: 0.658, lng: 34.585 },
  { id: "KCW-009", first_name: "Joseph", last_name: "Nyaga", county: "Meru", primary_crop: "avocado", farm_size_ha: 1.0, credit_score: 42.0, probability_default: 0.38, gender: "M", status: "active", chama_member: false, sacco_member: false, phone: "+254712345009", lat: 0.117, lng: 37.967 },
  { id: "KCW-010", first_name: "Faith", last_name: "Njeri", county: "Nyeri", primary_crop: "tea", farm_size_ha: 1.8, credit_score: 85.0, probability_default: 0.03, gender: "F", status: "active", chama_member: true, sacco_member: true, phone: "+254712345010", lat: -0.283, lng: 36.95 },
  { id: "KCW-011", first_name: "David", last_name: "Kiplagat", county: "Nakuru", primary_crop: "dairy", farm_size_ha: 6.0, credit_score: 73.0, probability_default: 0.10, gender: "M", status: "active", chama_member: false, sacco_member: true, phone: "+254712345011", lat: -0.717, lng: 36.433 },
  { id: "KCW-012", first_name: "Agnes", last_name: "Mwikali", county: "Kilifi", primary_crop: "tomato", farm_size_ha: 0.8, credit_score: 33.0, probability_default: 0.48, gender: "F", status: "delinquent", chama_member: true, sacco_member: false, phone: "+254712345012", lat: -3.017, lng: 39.967 },
  { id: "KCW-013", first_name: "Samuel", last_name: "Kipruto", county: "Uasin Gishu", primary_crop: "maize", farm_size_ha: 7.0, credit_score: 90.0, probability_default: 0.02, gender: "M", status: "completed", chama_member: false, sacco_member: true, phone: "+254712345013", lat: 0.517, lng: 35.267 },
  { id: "KCW-014", first_name: "Beatrice", last_name: "Akinyi", county: "Kisumu", primary_crop: "kale", farm_size_ha: 1.0, credit_score: 48.0, probability_default: 0.28, gender: "F", status: "active", chama_member: true, sacco_member: false, phone: "+254712345014", lat: -0.089, lng: 34.75 },
  { id: "KCW-015", first_name: "Patrick", last_name: "Muchiri", county: "Kiambu", primary_crop: "avocado", farm_size_ha: 2.0, credit_score: 65.0, probability_default: 0.14, gender: "M", status: "active", chama_member: true, sacco_member: true, phone: "+254712345015", lat: -1.1, lng: 37.017 },
];

const COUNTY_COORDS = {
  Kiambu: { x: 38, y: 52 }, Nakuru: { x: 33, y: 38 }, Kisumu: { x: 18, y: 45 },
  Meru: { x: 60, y: 25 }, Machakos: { x: 52, y: 55 }, "Uasin Gishu": { x: 30, y: 28 },
  "Homa Bay": { x: 20, y: 52 }, Bungoma: { x: 22, y: 22 }, Nyeri: { x: 40, y: 40 },
  Kilifi: { x: 70, y: 68 },
};

// ==============================
// State
// ==============================
let state = {
  farmers: MOCK_FARMERS,
  currentPage: "dashboard",
  theme: localStorage.getItem(THEME_KEY) || "light",
  lang: localStorage.getItem(LANG_KEY) || "en",
  searchQuery: "",
};

// ==============================
// DOM refs
// ==============================
const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

// ==============================
// Theme
// ==============================
function applyTheme(theme) {
  state.theme = theme;
  document.documentElement.classList.toggle("dark", theme === "dark");
  localStorage.setItem(THEME_KEY, theme);
  const btn = $("#theme-toggle");
  if (btn) btn.textContent = theme === "dark" ? "☀️" : "🌙";
}

// ==============================
// Language
// ==============================
function applyLanguage(lang) {
  state.lang = lang;
  setLanguage(lang);
  localStorage.setItem(LANG_KEY, lang);
  renderAll();
}

// ==============================
// Toast
// ==============================
function toast(message, type = "success", duration = 4000) {
  const container = $("#toast-container");
  const el = document.createElement("div");
  const bg = type === "success" ? "bg-green-600" : type === "error" ? "bg-red-600" : "bg-blue-600";
  el.className = `${bg} text-white px-4 py-3 rounded-lg shadow-lg text-sm flex items-center gap-2 animate-slide-in`;
  el.innerHTML = `<span>${type === "success" ? "✅" : type === "error" ? "❌" : "ℹ️"}</span><span>${message}</span>`;
  container.appendChild(el);
  setTimeout(() => { el.classList.add("animate-slide-out"); setTimeout(() => el.remove(), 300); }, duration);
}

// ==============================
// API
// ==============================
async function apiGet(path) {
  if (USE_MOCK) return null;
  try {
    const r = await fetch(`${API_BASE}${path}`, { signal: AbortSignal.timeout(5000) });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch { USE_MOCK = true; return null; }
}

async function apiPost(path, body) {
  if (USE_MOCK) return null;
  try {
    const r = await fetch(`${API_BASE}${path}`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body), signal: AbortSignal.timeout(10000),
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch { USE_MOCK = true; return null; }
}

// ==============================
// Navigation
// ==============================
function navigate(page) {
  state.currentPage = page;
  $$("[data-page]").forEach(el => el.classList.add("hidden"));
  const target = $(`[data-page="${page}"]`);
  if (target) target.classList.remove("hidden");
  $$(".nav-link").forEach(l => l.classList.toggle("active", l.dataset.nav === page));
  $$(".bottom-nav-link").forEach(l => l.classList.toggle("active", l.dataset.nav === page));
}

// ==============================
// Render: Dashboard
// ==============================
function renderDashboard() {
  const farmers = state.farmers;
  const active = farmers.filter(f => f.status === "active" || f.status === "completed");
  const vol = farmers.reduce((s, f) => s + (f.credit_score / 100) * 18000, 0);
  $("#stat-farmers").textContent = farmers.length;
  $("#stat-loans").textContent = active.length;
  $("#stat-volume").textContent = `KES ${(vol / 1000).toFixed(0)}K`;
  $("#stat-pools").textContent = "1";
  renderMap();
  renderPortfolioChart();
}

// ==============================
// Kenya Map
// ==============================
function renderMap() {
  const svg = document.getElementById("kenya-map-svg");
  if (!svg) return;
  const farmers = state.farmers;
  const countyCounts = {};
  farmers.forEach(f => { countyCounts[f.county] = (countyCounts[f.county] || 0) + 1; });
  const maxCount = Math.max(...Object.values(countyCounts), 1);

  svg.innerHTML = `
    <rect x="5" y="5" width="90" height="90" rx="4" fill="none" stroke="currentColor" stroke-width="0.5" class="text-gray-200 dark:text-gray-700" />
    <text x="50" y="12" text-anchor="middle" font-size="4" fill="currentColor" class="text-gray-400">KENYA</text>
    ${Object.entries(COUNTY_COORDS).map(([name, pos]) => {
      const count = countyCounts[name] || 0;
      const r = 3 + (count / maxCount) * 8;
      const opacity = 0.3 + (count / maxCount) * 0.7;
      return `<circle cx="${pos.x}" cy="${pos.y}" r="${r}" fill="#2E7D32" fill-opacity="${opacity}" stroke="#1B5E20" stroke-width="0.5" class="cursor-pointer hover:fill-opacity-90" title="${name}: ${count} farmers"/>
        <text x="${pos.x}" y="${pos.y + 14}" text-anchor="middle" font-size="3" fill="currentColor" class="text-gray-500 dark:text-gray-400">${name}</text>`;
    }).join("")}
  `;
}

// ==============================
// Portfolio Chart
// ==============================
function renderPortfolioChart() {
  const canvas = document.getElementById("portfolio-chart");
  if (!canvas) return;
  if (window._kcwChart) { window._kcwChart.destroy(); }
  window._kcwChart = new Chart(canvas.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Seeds", "Fertiliser", "Equipment", "Irrigation", "Livestock", "Transport"],
      datasets: [{
        label: "Loans", data: [8, 3, 4, 2, 1, 1],
        backgroundColor: ["#2E7D32", "#FFB300", "#5D4037", "#1565C0", "#C62828", "#6A1B9A"],
        borderRadius: 4,
      }],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { stepSize: 2 } } },
    },
  });
}

// ==============================
// Render: Farmers Table
// ==============================
function renderFarmers() {
  const tbody = document.getElementById("farmer-table-body");
  const query = (document.getElementById("farmer-search")?.value || "").toLowerCase();
  const filtered = state.farmers.filter(f =>
    !query || f.id.toLowerCase().includes(query) || f.first_name.toLowerCase().includes(query) ||
    f.last_name.toLowerCase().includes(query) || f.county.toLowerCase().includes(query)
  );
  tbody.innerHTML = filtered.map(f => {
    const icon = f.gender === "F" ? t("female_icon") : t("male_icon");
    const badge = f.status === "active"
      ? `<span class="badge badge-green">${t("status_active")}</span>`
      : f.status === "delinquent"
        ? `<span class="badge badge-red">${t("status_delinquent")}</span>`
        : `<span class="badge badge-blue">${t("status_completed")}</span>`;
    const pd = (f.probability_default * 100).toFixed(1);
    return `<tr class="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
      <td class="py-2.5 pr-2 text-xs font-mono text-gray-500">${f.id}</td>
      <td class="py-2.5 pr-2 font-medium">${icon} ${f.first_name} ${f.last_name}</td>
      <td class="py-2.5 pr-2">${f.county}</td>
      <td class="py-2.5 pr-2 hidden sm:table-cell">${f.primary_crop}</td>
      <td class="py-2.5 pr-2 font-mono">${f.credit_score}</td>
      <td class="py-2.5 pr-2 hidden sm:table-cell font-mono">${pd}%</td>
      <td class="py-2.5">${badge}</td>
    </tr>`;
  }).join("");
  document.getElementById("farmer-count").textContent = filtered.length === state.farmers.length
    ? t("farmers_count", state.farmers.length)
    : `${filtered.length} / ${t("farmers_count", state.farmers.length)}`;
}

// ==============================
// Render: Escrow
// ==============================
function renderEscrow() {
  const states = [
    { name: "FundsLockingRequested", done: true, desc: t("escrow_initiated") },
    { name: "FundsLocked", done: true, desc: t("escrow_locked") },
    { name: "ResultSubmitted", done: true, desc: t("escrow_submitted") },
    { name: "Completed", done: false, desc: t("escrow_completed") },
  ];
  const el = document.getElementById("escrow-list");
  if (!el) return;
  el.innerHTML = `<p class="text-xs text-gray-400 mb-3">${t("escrow_desc")}</p>${
    states.map((s, i) => {
      const isLast = i === states.length - 1;
      return `<div class="flex items-center gap-3 p-3 rounded-lg ${s.done && !isLast ? 'bg-green-50 dark:bg-green-900/20' : 'bg-gray-50 dark:bg-gray-800'} transition-colors">
        <span class="text-base flex-shrink-0">${s.done && !isLast ? '✅' : '⏳'}</span>
        <div class="min-w-0 flex-1">
          <p class="text-sm font-medium truncate">${s.name}</p>
          <p class="text-xs text-gray-400 truncate">${s.desc}</p>
        </div>
        <span class="text-xs flex-shrink-0 ${s.done && !isLast ? 'text-green-600' : 'text-gray-400'}">${s.done && !isLast ? t("escrow_complete_label") : isLast ? t("escrow_ready") : t("escrow_waiting")}</span>
      </div>`;
    }).join("")
  }`;
}

// ==============================
// Handlers
// ==============================
async function handleAssessmentSubmit(e) {
  e.preventDefault();
  const form = e.target;
  if (!form.checkValidity()) { form.reportValidity(); return; }

  const formData = new FormData(form);
  const data = Object.fromEntries(formData);
  data.chama_member = form.chama_member.checked;
  data.sacco_member = form.sacco_member.checked;
  data.farm_size_ha = parseFloat(data.farm_size_ha);
  data.latitude = -1.0;
  data.longitude = 36.9;

  const btn = document.getElementById("assess-submit");
  btn.disabled = true;
  btn.innerHTML = `<span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span> ${t("assess_processing")}`;

  const resultDiv = document.getElementById("assessment-result");
  resultDiv.classList.add("hidden");

  try {
    const resp = await apiPost("/apply", data);
    const score = resp?.assessment?.credit_score ?? Math.round(40 + Math.random() * 50);
    const pd = resp?.assessment?.probability_default ?? ((100 - score) / 100);
    const approved = resp?.status === "approved" || score >= 50;
    const statusColor = approved ? "green" : "red";

    resultDiv.innerHTML = `
      <div class="bg-${statusColor}-50 dark:bg-${statusColor}-900/20 border border-${statusColor}-200 dark:border-${statusColor}-800 rounded-xl p-4 text-sm transition-all">
        <div class="flex items-center gap-2 mb-3">
          <span class="text-lg">${approved ? "✅" : "❌"}</span>
          <span class="font-bold text-${statusColor}-800 dark:text-${statusColor}-300">${approved ? t("approved") : t("declined")}</span>
          ${USE_MOCK ? '<span class="badge badge-gold ml-auto">' + t("mock_badge") + '</span>' : ""}
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <div><span class="text-gray-500 text-xs">${t("credit_score")}</span><br><strong>${score}</strong></div>
          <div><span class="text-gray-500 text-xs">PD</span><br><strong>${(typeof pd === "number" ? pd : 0).toFixed(2)}</strong></div>
          <div><span class="text-gray-500 text-xs">${t("max_loan")}</span><br><strong>KES ${(data.farm_size_ha * 12000).toFixed(0)}</strong></div>
        </div>
      </div>`;
    resultDiv.classList.remove("hidden");
    toast(approved ? t("toast_assess_done") : t("toast_assess_error"), approved ? "success" : "error");
  } catch (err) {
    resultDiv.innerHTML = `<div class="bg-red-50 dark:bg-red-900/20 border border-red-200 rounded-xl p-4 text-sm text-red-700 dark:text-red-300">${t("error_prefix")}: ${err.message}</div>`;
    resultDiv.classList.remove("hidden");
    toast(t("toast_assess_error"), "error");
  } finally {
    btn.disabled = false;
    btn.textContent = t("assess_submit");
  }
}

async function handleBuildPool() {
  const btn = document.getElementById("build-pool-btn");
  btn.disabled = true;
  btn.innerHTML = `<span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span> ${t("pool_building")}`;

  try {
    const approved = state.farmers.filter(f => f.status === "active" && f.credit_score >= 50);
    const farmerData = approved.map(f => ({
      id: f.id, max_loan_kes: (f.credit_score / 100) * 18000,
      probability_default: f.probability_default, interest_rate_annual: 18.0,
    }));
    const resp = await apiPost("/pools/build", { farmer_data: farmerData });

    const pool = resp ?? {
      name: "KCW Demo Pool", farmer_count: approved.length,
      total_notional_kes: approved.length * 17942, avg_pd: 0.14,
      expected_revenue_kes: Math.round(approved.length * 17942 * 1.18 * 0.86), target_rating: "BBB-",
    };

    const el = document.getElementById("pool-result");
    el.classList.remove("hidden");
    el.innerHTML = `
      <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl p-4 text-sm">
        <div class="flex items-center gap-2 mb-3">
          <span>✅</span>
          <span class="font-bold text-green-800 dark:text-green-300">${pool.name || "KCW Pool"}</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <div><span class="text-gray-500 text-xs">${t("pool_farmers")}</span><br><strong>${pool.farmer_count}</strong></div>
          <div><span class="text-gray-500 text-xs">${t("pool_notional")}</span><br><strong>KES ${(pool.total_notional_kes / 1000).toFixed(0)}K</strong></div>
          <div><span class="text-gray-500 text-xs">${t("pool_avg_pd")}</span><br><strong>${(pool.avg_pd * 100).toFixed(1)}%</strong></div>
          <div><span class="text-gray-500 text-xs">${t("pool_revenue")}</span><br><strong>KES ${(pool.expected_revenue_kes / 1000).toFixed(0)}K</strong></div>
          <div><span class="text-gray-500 text-xs">${t("pool_rating")}</span><br><span class="badge badge-gold">${pool.target_rating}</span></div>
        </div>
      </div>`;
    toast(t("toast_pool_built"), "success");
  } catch (err) {
    toast(t("toast_pool_error"), "error");
  } finally {
    btn.disabled = false;
    btn.innerHTML = t("pool_build");
  }
}

// ==============================
// Render All
// ==============================
function renderAll() {
  renderDashboard();
  renderFarmers();
  renderEscrow();
  renderFarmers(); // re-render with new lang
  // update text nodes
  $$("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
  $$("[data-i18n-placeholder]").forEach(el => { el.placeholder = t(el.dataset.i18nPlaceholder); });
  // update submit button
  const btn = document.getElementById("assess-submit");
  if (btn && !btn.disabled) btn.textContent = t("assess_submit");
}

// ==============================
// Init
// ==============================
document.addEventListener("DOMContentLoaded", () => {
  // Restore saved language
  applyLanguage(state.lang);

  // Restore saved theme
  applyTheme(state.theme);

  // Search
  document.getElementById("farmer-search")?.addEventListener("input", renderFarmers);

  // Navigation
  $$(".nav-link, .bottom-nav-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      navigate(link.dataset.nav);
    });
  });

  // Theme toggle
  document.getElementById("theme-toggle")?.addEventListener("click", () => {
    applyTheme(state.theme === "light" ? "dark" : "light");
  });

  // Language toggle
  document.getElementById("lang-toggle")?.addEventListener("click", () => {
    applyLanguage(state.lang === "en" ? "sw" : "en");
  });

  // Forms
  document.getElementById("assessment-form")?.addEventListener("submit", handleAssessmentSubmit);
  document.getElementById("build-pool-btn")?.addEventListener("click", handleBuildPool);

  // Initial render
  navigate("dashboard");
  renderAll();

  // Set language toggle text
  const langBtn = document.getElementById("lang-toggle");
  if (langBtn) langBtn.textContent = state.lang === "en" ? "SW" : "EN";
});
