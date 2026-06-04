export const LANGUAGES = { en: "English", sw: "Kiswahili" };

const TR = {
  en: {
    app_name: "Food Roots KE",
    loading: "Loading...",
    nav_dashboard: "Dashboard",
    nav_foods: "Traditional Foods",
    nav_corridors: "Food Corridors",
    nav_market: "Marketplace",
    nav_derisk: "De-Risk",
    nairobi_pct: "Of ~680 foods eaten by Nairobians, only ~⅓ are indigenous to Kenya",
    stats_crops: "Crops Indexed",
    stats_indigenous: "Indigenous",
    stats_corridors: "Food Corridors",
    stats_tests: "Tests Passing",
  },
  sw: {
    app_name: "Food Roots KE",
    loading: "Inapakia...",
    nav_dashboard: "Dashibodi",
    nav_foods: "Vyakula Asili",
    nav_corridors: "Korido za Chakula",
    nav_market: "Soko",
    nav_derisk: "Kupunguza Hatari",
    nairobi_pct: "Kati ya vyakula ~680 vinavyoliwa Nairobeni, ~⅓ tu ni asili ya Kenya",
    stats_crops: "Mimea Iliyoorodheshwa",
    stats_indigenous: "Asili",
    stats_corridors: "Korido za Chakula",
    stats_tests: "Majaribio Yaliyofaulu",
  },
};

let _lang = "en";

export function setLanguage(l) { if (TR[l]) _lang = l; }

export function t(key, ...args) {
  let msg = TR[_lang]?.[key] ?? TR.en[key] ?? key;
  if (args.length) msg = msg.replace("{n}", args[0]);
  return msg;
}

export function currentLang() { return _lang; }
