(function () {
  "use strict";

  // This file is loaded synchronously right after leaflet.js in the page body,
  // before Blowfish's deferred head scripts run and overwrite window.L.
  var Leaflet = window.L;
  if (!Leaflet || !Leaflet.version || typeof Leaflet.map !== "function" || Leaflet.map === Array.prototype.map) {
    document.addEventListener("DOMContentLoaded", function () {
      var meta = document.getElementById("qso-map-meta");
      if (meta) meta.textContent = "Kunde inte ladda QSO-data.";
    });
    return;
  }

  var BAND_COLORS = {
    "160m": "#7c3aed", "80m": "#2563eb", "60m": "#0891b2", "40m": "#059669",
    "30m": "#65a30d", "20m": "#ca8a04", "17m": "#ea580c", "15m": "#dc2626",
    "12m": "#db2777", "10m": "#c026d3", "6m": "#4f46e5", "2m": "#0ea5e9"
  };
  var FALLBACK = "#64748b";
  var i18n = {
    sv: {
      plotted: "QSO på kartan", confirmed: "bekräftade", dxcc: "DXCC",
      updated: "Uppdaterad", home: "Hemmastation", noData: "Kunde inte ladda QSO-data.",
      band: "Band", mode: "Mode", date: "Datum", grid: "Ruta", country: "Land"
    },
    en: {
      plotted: "QSOs on map", confirmed: "confirmed", dxcc: "DXCC",
      updated: "Updated", home: "Home station", noData: "Could not load QSO data.",
      band: "Band", mode: "Mode", date: "Date", grid: "Grid", country: "Country"
    }
  };

  function t10n() {
    var lang = (document.documentElement.lang || "sv").slice(0, 2);
    return i18n[lang] || i18n.en;
  }
  function fmtDate(yyyymmdd) {
    if (!yyyymmdd || yyyymmdd.length < 8) return yyyymmdd || "";
    return yyyymmdd.slice(0, 4) + "-" + yyyymmdd.slice(4, 6) + "-" + yyyymmdd.slice(6, 8);
  }
  function colorFor(band) {
    return BAND_COLORS[(band || "").toLowerCase()] || FALLBACK;
  }

  var el = document.getElementById("qso-map");
  var meta = document.getElementById("qso-map-meta");
  if (!el || !meta) return;

  // Build the map NOW while window.L is still Leaflet.
  window.L = Leaflet;
  var map = Leaflet.map(el, { scrollWheelZoom: true, worldCopyJump: true }).setView([54, 10], 4);
  var lightTiles = Leaflet.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  });
  var darkTiles = Leaflet.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>'
  });
  function isDark() {
    return document.documentElement.classList.contains("dark");
  }
  (isDark() ? darkTiles : lightTiles).addTo(map);
  var group = Leaflet.layerGroup().addTo(map);

  Promise.all([
    fetch("/data/qsos.json").then(function (r) { if (!r.ok) throw new Error("qsos"); return r.json(); }),
    fetch("/data/qso-summary.json").then(function (r) { if (!r.ok) throw new Error("summary"); return r.json(); })
  ]).then(function (pair) {
    window.L = Leaflet;
    var t = t10n();
    var qsos = pair[0];
    var summary = pair[1];
    var generated = summary.generated ? summary.generated.replace("T", " ").replace("Z", " UTC") : "";
    meta.innerHTML =
      "<span><strong>" + summary.plotted + "</strong> " + t.plotted + "</span>" +
      "<span><strong>" + (summary.confirmed || 0) + "</strong> " + t.confirmed + "</span>" +
      "<span><strong>" + (summary.dxcc || 0) + "</strong> " + t.dxcc + "</span>" +
      (generated ? "<span>" + t.updated + ": " + generated + "</span>" : "");

    var bounds = [];
    qsos.forEach(function (q) {
      if (typeof q.lat !== "number" || typeof q.lon !== "number") return;
      var marker = Leaflet.circleMarker([q.lat, q.lon], {
        radius: 5,
        color: q.confirmed ? "#fbbf24" : "#ffffff",
        weight: 1.5,
        fillColor: colorFor(q.band),
        fillOpacity: 0.85
      });
      var lines = ["<div class='qso-popup'><strong>" + (q.call || "") + "</strong>"];
      if (q.band || q.mode) {
        lines.push("<div>" + t.band + ": " + (q.band || "-") + " · " + t.mode + ": " + (q.mode || "-") + "</div>");
      }
      if (q.date) {
        lines.push("<div>" + t.date + ": " + fmtDate(q.date) +
          (q.time ? " " + q.time.slice(0, 2) + ":" + q.time.slice(2, 4) + " UTC" : "") + "</div>");
      }
      if (q.grid) lines.push("<div>" + t.grid + ": " + q.grid + "</div>");
      if (q.country) lines.push("<div>" + t.country + ": " + q.country + "</div>");
      lines.push("</div>");
      marker.bindPopup(lines.join(""));
      group.addLayer(marker);
      bounds.push([q.lat, q.lon]);
    });

    if (summary.home && typeof summary.home.lat === "number") {
      var home = Leaflet.circleMarker([summary.home.lat, summary.home.lon], {
        radius: 8,
        color: "#ffffff",
        weight: 2,
        fillColor: "#f59e0b",
        fillOpacity: 1
      });
      home.bindPopup(
        "<div class='qso-popup'><strong>" + (summary.home.label || "SM4T") + "</strong><div>" +
        t.home + (summary.home.grid ? " · " + summary.home.grid : "") + "</div></div>"
      );
      home.addTo(map);
      bounds.push([summary.home.lat, summary.home.lon]);
    }

    if (bounds.length) map.fitBounds(bounds, { padding: [28, 28], maxZoom: 6 });
    map.invalidateSize();

    var legend = document.getElementById("qso-map-legend");
    if (legend) {
      var bands = Object.keys(summary.bands || {});
      legend.innerHTML = bands.map(function (b) {
        return '<span><i class="qso-map-swatch" style="background:' + colorFor(b) + '"></i>' + b + "</span>";
      }).join("") +
        '<span><i class="qso-map-swatch" style="background:#f59e0b"></i>' + t.home + "</span>";
    }

    new MutationObserver(function () {
      var wantDark = isDark();
      if (wantDark && map.hasLayer(lightTiles)) { map.removeLayer(lightTiles); darkTiles.addTo(map); }
      if (!wantDark && map.hasLayer(darkTiles)) { map.removeLayer(darkTiles); lightTiles.addTo(map); }
    }).observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
  }).catch(function (err) {
    var t = t10n();
    meta.textContent = t.noData;
    if (window.console && console.error) console.error("qso-map", err);
  });
})();
