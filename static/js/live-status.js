(function () {
  "use strict";

  // Capture Leaflet now, before Blowfish's deferred head scripts overwrite window.L.
  var Leaflet = window.L;
  var QRV_SECONDS = 30 * 60;
  var BAND_COLORS = {
    "160m": "#7c3aed", "80m": "#2563eb", "60m": "#0891b2", "40m": "#059669",
    "30m": "#65a30d", "20m": "#ca8a04", "17m": "#ea580c", "15m": "#dc2626",
    "12m": "#db2777", "10m": "#c026d3", "6m": "#4f46e5", "2m": "#0ea5e9"
  };
  var FALLBACK = "#64748b";
  var PSK_COLOR = "#0ea5e9";
  var COUNTRY_SV = {
    "Canary Is.": "Kanarieöarna",
    "Canary Islands": "Kanarieöarna",
    "Asiatic Russia": "Asiatiska Ryssland",
    "European Russia": "Europeiska Ryssland",
    "England": "England",
    "Scotland": "Skottland",
    "Wales": "Wales",
    "Ireland": "Irland",
    "Northern Ireland": "Nordirland",
    "Germany": "Tyskland",
    "France": "Frankrike",
    "Spain": "Spanien",
    "Italy": "Italien",
    "Sweden": "Sverige",
    "Norway": "Norge",
    "Denmark": "Danmark",
    "Finland": "Finland",
    "Poland": "Polen",
    "Netherlands": "Nederländerna",
    "Belgium": "Belgien",
    "Austria": "Österrike",
    "Switzerland": "Schweiz",
    "Czech Republic": "Tjeckien",
    "Slovak Republic": "Slovakien",
    "Hungary": "Ungarn",
    "Romania": "Rumänien",
    "Bulgaria": "Bulgarien",
    "Greece": "Grekland",
    "Portugal": "Portugal",
    "Ukraine": "Ukraina",
    "Belarus": "Belarus",
    "Lithuania": "Litauen",
    "Latvia": "Lettland",
    "Estonia": "Estland",
    "Iceland": "Island",
    "United States": "USA",
    "Canada": "Kanada",
    "Japan": "Japan",
    "China": "Kina",
    "Australia": "Australien",
    "New Zealand": "Nya Zeeland",
    "South Africa": "Sydafrika",
    "Brazil": "Brasilien",
    "Argentina": "Argentina",
    "Turkey": "Turkiet",
    "Croatia": "Kroatien",
    "Slovenia": "Slovenien",
    "Serbia": "Serbien",
    "Bosnia and Herzegovina": "Bosnien och Hercegovina",
    "Faroe Islands": "Färöarna",
    "Svalbard": "Svalbard",
    "Aland Islands": "Åland",
    "Luxembourg": "Luxemburg"
  };

  var i18n = {
    sv: { home: "QTH", spots: "spots", spot: "spot", reports: "rapporter", report: "rapport" },
    en: { home: "QTH", spots: "spots", spot: "spot", reports: "reports", report: "report" }
  };

  function lang() {
    return (document.documentElement.lang || "sv").slice(0, 2);
  }
  function t(key) {
    return (i18n[lang()] || i18n.en)[key] || key;
  }
  function countryName(name) {
    if (!name) return "";
    return lang() === "sv" ? (COUNTRY_SV[name] || name) : name;
  }
  function colorFor(band) {
    return BAND_COLORS[(band || "").toLowerCase()] || FALLBACK;
  }
  function bandLabel(band) {
    if (!band) return "";
    return String(band).replace(/m$/i, " m");
  }

  function readData() {
    var el = document.getElementById("live-status-data");
    if (!el) return null;
    try {
      var data = JSON.parse(el.textContent || "");
      if (typeof data === "string") data = JSON.parse(data);
      return data && typeof data === "object" ? data : null;
    } catch (err) {
      return null;
    }
  }

  function lastHeardEpoch(data) {
    var rbn = data && data.rbn;
    if (!rbn || !rbn.ok || !rbn.lastHeard) return 0;
    return Number(rbn.lastHeard.epoch || 0);
  }

  function refreshQrv(data) {
    var badge = document.getElementById("live-status-qrv");
    if (!badge) return;
    var epoch = lastHeardEpoch(data);
    var now = Math.floor(Date.now() / 1000);
    var on = epoch > 0 && (now - epoch) <= QRV_SECONDS;
    badge.hidden = !on;
    badge.classList.toggle("is-hidden", !on);
  }

  function initMap(data) {
    var holder = document.getElementById("live-status-map");
    if (!holder) return;
    if (!Leaflet || !Leaflet.version || typeof Leaflet.map !== "function" || Leaflet.map === Array.prototype.map) {
      holder.style.display = "none";
      return;
    }

    var points = [];
    var rbn = (data.rbn && data.rbn.ok && data.rbn.skimmers) || [];
    rbn.forEach(function (s) {
      if (typeof s.lat === "number" && typeof s.lon === "number") points.push({ kind: "rbn", s: s });
    });
    var psk = (data.psk && data.psk.ok && data.psk.receivers) || [];
    psk.forEach(function (s) {
      if (typeof s.lat === "number" && typeof s.lon === "number") points.push({ kind: "psk", s: s });
    });
    if (!points.length) {
      holder.style.display = "none";
      return;
    }

    var map = Leaflet.map(holder, { scrollWheelZoom: false, attributionControl: true });
    Leaflet.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap",
      maxZoom: 8
    }).addTo(map);

    var bounds = Leaflet.latLngBounds([]);
    var home = data.home;
    if (home && typeof home.lat === "number" && typeof home.lon === "number") {
      var homeIcon = Leaflet.divIcon({
        className: "live-status-home-icon",
        html: '<span style="display:block;width:12px;height:12px;border-radius:2px;background:#0f172a;border:2px solid #f8fafc;box-shadow:0 0 0 1px rgba(0,0,0,.35);transform:rotate(45deg);"></span>',
        iconSize: [12, 12],
        iconAnchor: [6, 6]
      });
      Leaflet.marker([home.lat, home.lon], { icon: homeIcon, zIndexOffset: 200, title: "SM4T" })
        .bindPopup('<div class="live-status-popup"><strong>SM4T</strong><br>' + t("home") + (home.grid ? " " + home.grid : "") + "</div>")
        .addTo(map);
      bounds.extend([home.lat, home.lon]);
    }

    points.forEach(function (pt) {
      var s = pt.s;
      var color = pt.kind === "psk" ? PSK_COLOR : colorFor(s.lastBand);
      var radius = pt.kind === "psk" ? 5 : 6;
      var label = s.call || s.locator || "";
      var count = s.count || 0;
      var countWord = count === 1 ? (pt.kind === "psk" ? t("report") : t("spot")) : (pt.kind === "psk" ? t("reports") : t("spots"));
      var bits = ["<div class=\"live-status-popup\"><strong>" + label + "</strong>"];
      if (s.country) bits.push(countryName(s.country));
      if (s.lastBand || s.lastSnr != null) {
        bits.push(
          [bandLabel(s.lastBand), s.lastSnr != null ? s.lastSnr + " dB" : ""]
            .filter(Boolean)
            .join(", ")
        );
      }
      if (s.km != null) bits.push(s.km.toLocaleString(lang() === "sv" ? "sv-SE" : "en-GB") + " km");
      if (count) bits.push(count + " " + countWord);
      bits.push("</div>");
      Leaflet.circleMarker([s.lat, s.lon], {
        radius: radius,
        color: "#fff",
        weight: 1,
        fillColor: color,
        fillOpacity: 0.9
      }).bindPopup(bits.join("<br>")).addTo(map);
      bounds.extend([s.lat, s.lon]);
    });

    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [16, 16], maxZoom: 5 });
    } else {
      map.setView([60.5, 15.5], 3);
    }
    setTimeout(function () { map.invalidateSize(); }, 0);
  }

  var data = readData();
  if (!data) return;
  refreshQrv(data);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { initMap(data); });
  } else {
    initMap(data);
  }
})();
