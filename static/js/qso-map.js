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
      updated: "Uppdaterad", home: "Home QTH", noData: "Kunde inte ladda QSO-data.", legend: "Band", latest: "Senaste 20 QSO", stats: "Statistik", total: "QSO totalt", bandsN: "band", firstQso: "Första QSO med callsign SM4T", perBand: "QSO per band", topCountries: "Flest QSO per DXCC",
      band: "Band", mode: "Mode", date: "Datum", grid: "Ruta", country: "Land", perMonth: "QSO per månad", monthTotal: "totalt"
    },
    en: {
      plotted: "QSOs on map", confirmed: "confirmed", dxcc: "DXCC",
      updated: "Updated", home: "Home QTH", noData: "Could not load QSO data.", legend: "Band", latest: "Latest 20 QSOs", stats: "Statistics", total: "QSOs in total", bandsN: "bands", firstQso: "First QSO as SM4T", perBand: "QSOs per band", topCountries: "Most QSOs by DXCC entity",
      band: "Band", mode: "Mode", date: "Date", grid: "Grid", country: "Country", perMonth: "QSOs per month", monthTotal: "total"
    }
  };

  var COUNTRY_SV = {"Asiatic Russia": "Asiatiska Ryssland", "Australia": "Australien", "Austria": "Österrike", "Balearic Islands": "Balearerna", "Belarus": "Belarus", "Belgium": "Belgien", "Bosnia and Herzegovina": "Bosnien och Hercegovina", "Bulgaria": "Bulgarien", "Canary Islands": "Kanarieöarna", "China": "Kina", "Croatia": "Kroatien", "Czech Republic": "Tjeckien", "Denmark": "Danmark", "England": "England", "Estonia": "Estland", "Finland": "Finland", "France": "Frankrike", "Galapagos Islands": "Galápagosöarna", "Georgia": "Georgien", "Germany": "Tyskland", "Greece": "Grekland", "Hungary": "Ungern", "Indonesia": "Indonesien", "Ireland": "Irland", "Israel": "Israel", "Italy": "Italien", "Japan": "Japan", "Latvia": "Lettland", "Lithuania": "Litauen", "Mali": "Mali", "Moldova": "Moldavien", "Monaco": "Monaco", "Montenegro": "Montenegro", "Morocco": "Marocko", "Netherlands": "Nederländerna", "North Macedonia (Republic of)": "Nordmakedonien", "Poland": "Polen", "Portugal": "Portugal", "Republic of Kosovo": "Kosovo", "Rodriguez Island": "Rodrigues", "Romania": "Rumänien", "Russia": "Ryssland", "European Russia": "Europeiska Ryssland", "Scotland": "Skottland", "Serbia": "Serbien", "Slovak Republic": "Slovakien", "Slovenia": "Slovenien", "Spain": "Spanien", "Svalbard": "Svalbard", "Sweden": "Sverige", "Switzerland": "Schweiz", "Turkey": "Turkiet", "Ukraine": "Ukraina", "United States": "USA", "Wales": "Wales", "Norway": "Norge", "Iceland": "Island", "Faroe Islands": "Färöarna", "Aland Islands": "Åland", "Greenland": "Grönland", "Canada": "Kanada", "Brazil": "Brasilien", "Argentina": "Argentina", "Chile": "Chile", "Mexico": "Mexiko", "South Africa": "Sydafrika", "New Zealand": "Nya Zeeland", "Luxembourg": "Luxemburg", "Liechtenstein": "Liechtenstein", "Andorra": "Andorra", "San Marino": "San Marino", "Vatican City": "Vatikanstaten", "Malta": "Malta", "Cyprus": "Cypern", "Albania": "Albanien", "Northern Ireland": "Nordirland", "Isle of Man": "Isle of Man", "Jersey": "Jersey", "Guernsey": "Guernsey", "Gibraltar": "Gibraltar", "Sardinia": "Sardinien", "Sicily": "Sicilien", "Corsica": "Korsika", "Crete": "Kreta", "Madeira Islands": "Madeira", "Azores": "Azorerna", "Kaliningrad": "Kaliningrad", "Kazakhstan": "Kazakstan", "Armenia": "Armenien", "Azerbaijan": "Azerbajdzjan", "India": "Indien", "Thailand": "Thailand", "Philippines": "Filippinerna", "South Korea": "Sydkorea", "Republic of Korea": "Sydkorea", "Taiwan": "Taiwan", "Egypt": "Egypten", "Tunisia": "Tunisien", "Algeria": "Algeriet", "Lebanon": "Libanon", "Jordan": "Jordanien", "Saudi Arabia": "Saudiarabien", "United Arab Emirates": "Förenade Arabemiraten", "Cuba": "Kuba", "Puerto Rico": "Puerto Rico", "Hawaii": "Hawaii", "Alaska": "Alaska", "Uruguay": "Uruguay", "Venezuela": "Venezuela", "Colombia": "Colombia", "Peru": "Peru", "Ecuador": "Ecuador"};
  function countryName(c) {
    if (!c) return c;
    var lang = (document.documentElement.lang || "sv").slice(0, 2);
    return lang === "sv" ? (COUNTRY_SV[c] || c) : c;
  }

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
  // Use the same key-free OpenStreetMap background in both site themes.
  Leaflet.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'
  }).addTo(map);
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


    var statsEl = document.getElementById("qso-stats");
    if (statsEl && qsos.length) {
      var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]; }); };
      var countryCounts = {};
      var first = "";
      qsos.forEach(function (q) {
        if (q.country) { var cn = countryName(q.country); countryCounts[cn] = (countryCounts[cn] || 0) + 1; }
        if (q.date && (!first || q.date < first)) first = q.date;
      });
      var bandOrderS = ["160m","80m","60m","40m","30m","20m","17m","15m","12m","10m","6m","4m","2m","70cm"];
      var bandList = Object.keys(summary.bands || {}).sort(function (a, b) {
        var ia = bandOrderS.indexOf(a), ib = bandOrderS.indexOf(b);
        return (ia < 0 ? 999 : ia) - (ib < 0 ? 999 : ib);
      });
      var maxBand = Math.max.apply(null, bandList.map(function (b) { return summary.bands[b]; }).concat([1]));
      var topC = Object.keys(countryCounts).sort(function (a, b) { return countryCounts[b] - countryCounts[a] || a.localeCompare(b); }).slice(0, 10);
      var maxC = topC.length ? countryCounts[topC[0]] : 1;
      var bar = function (name, n, max, color) {
        return '<div class="qso-bar"><span class="qso-bar-name">' + esc(name) + '</span><span class="qso-bar-track"><span class="qso-bar-fill" style="display:block;width:' +
          Math.max(3, Math.round(100 * n / max)) + '%;background:' + color + '"></span></span><span class="qso-bar-count">' + n + "</span></div>";
      };
      var num = function (n, label) { return '<div class="qso-stats-num"><strong>' + n + "</strong><span>" + label + "</span></div>"; };
      statsEl.innerHTML =
        '<div class="qso-stats-box"><h3>' + t.stats + '</h3><div class="qso-stats-nums">' +
          num(summary.totalInLog || qsos.length, t.total) +
          num(summary.confirmed || 0, t.confirmed) +
          num(summary.dxcc || Object.keys(countryCounts).length, t.dxcc) +
          num(bandList.length, t.bandsN) +
          (first ? num(fmtDate(first), t.firstQso).replace("qso-stats-num\"", "qso-stats-num wide\"") : "") +
        "</div></div>" +
        '<div class="qso-stats-box"><h3>' + t.perBand + "</h3>" +
          bandList.map(function (b) { return bar(b, summary.bands[b], maxBand, colorFor(b)); }).join("") + "</div>" +
        '<div class="qso-stats-box"><h3>' + t.topCountries + "</h3>" +
          topC.map(function (c) { return bar(c, countryCounts[c], maxC, "#0ea5e9"); }).join("") + "</div>";
      statsEl.hidden = false;
    }

    var latestWrap = document.getElementById("qso-latest");
    var latestTitle = document.getElementById("qso-latest-title");
    var latestList = document.getElementById("qso-latest-list");
    if (latestWrap && latestTitle && latestList) {
      var latest = qsos.slice().sort(function (a, b) {
        var da = (a.date || "") + (a.time || "");
        var db = (b.date || "") + (b.time || "");
        return db < da ? -1 : db > da ? 1 : 0;
      }).slice(0, 20);
      latestTitle.textContent = t.latest;
      latestList.innerHTML = latest.map(function (q) {
        return "<li><span class=\"qso-latest-call\">" + (q.call || "") +
          "</span><span class=\"qso-latest-band\">" + (q.band || "-") +
          "</span><span class=\"qso-latest-mode\">" + (q.mode || "-") +
          "</span><span class=\"qso-latest-country\">" + (countryName(q.country) || "-") +
          "</span><span class=\"qso-latest-date\">" + (fmtDate(q.date) || "-") +
          (q.time ? " " + q.time.slice(0, 2) + ":" + q.time.slice(2, 4) + " UTC" : "") + "</span></li>";
      }).join("");
      latestWrap.hidden = latest.length === 0;
    }


    renderMonthlyChart(qsos);

    var bounds = [];
    qsos.forEach(function (q) {
      if (typeof q.lat !== "number" || typeof q.lon !== "number") return;
      // 0,0 means "position unknown" in QRZ data; never plot it.
      if (Math.abs(q.lat) < 1e-6 && Math.abs(q.lon) < 1e-6) return;
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
      if (q.country) lines.push("<div>" + t.country + ": " + countryName(q.country) + "</div>");
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

    var bandOrder = ["160m","80m","60m","40m","30m","20m","17m","15m","12m","10m","6m","4m","2m","70cm"];
    var bands = Object.keys(summary.bands || {}).sort(function (a, b) {
      var ia = bandOrder.indexOf(a), ib = bandOrder.indexOf(b);
      if (ia < 0) ia = 999;
      if (ib < 0) ib = 999;
      if (ia !== ib) return ia - ib;
      return a.localeCompare(b);
    });
    var Legend = Leaflet.Control.extend({
      options: { position: "bottomleft" },
      onAdd: function () {
        var div = Leaflet.DomUtil.create("div", "qso-band-legend");
        div.setAttribute("aria-label", t.legend);
        var html = '<div class="qso-band-legend-title">' + t.legend + "</div>";
        bands.forEach(function (b) {
          html += '<div class="qso-band-legend-row"><span class="qso-band-legend-swatch" style="background:' +
            colorFor(b) + '"></span><span>' + b + "</span></div>";
        });
        html += '<div class="qso-band-legend-row"><span class="qso-band-legend-swatch" style="background:#f59e0b"></span><span>' +
          t.home + "</span></div>";
        div.innerHTML = html;
        Leaflet.DomEvent.disableClickPropagation(div);
        Leaflet.DomEvent.disableScrollPropagation(div);
        return div;
      }
    });
    new Legend().addTo(map);

  }).catch(function (err) {
    var t = t10n();
    meta.textContent = t.noData;
    if (window.console && console.error) console.error("qso-map", err);
  });

  var MONTHS_SV = ["jan","feb","mar","apr","maj","jun","jul","aug","sep","okt","nov","dec"];
  var MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var BAND_ORDER = ["160m","80m","60m","40m","30m","20m","17m","15m","12m","10m","6m","4m","2m","70cm"];
  var monthlyState = null;

  function pad2(n) { return (n < 10 ? "0" : "") + n; }
  function yyyymmFromDateStr(d) { return (d || "").slice(0, 6); }
  function yyyymmFromDate(d) {
    return String(d.getUTCFullYear()) + pad2(d.getUTCMonth() + 1);
  }
  function nextMonth(yyyymm) {
    var y = parseInt(yyyymm.slice(0, 4), 10);
    var m = parseInt(yyyymm.slice(4, 6), 10) + 1;
    if (m > 12) { m = 1; y += 1; }
    return String(y) + pad2(m);
  }
  function monthList(from, to) {
    var out = [];
    var cur = from;
    while (cur && cur <= to) {
      out.push(cur);
      cur = nextMonth(cur);
      if (out.length > 600) break;
    }
    return out;
  }
  function monthLabel(yyyymm, lang, part) {
    var m = parseInt(yyyymm.slice(4, 6), 10);
    var names = lang === "sv" ? MONTHS_SV : MONTHS_EN;
    var name = names[m - 1] || yyyymm.slice(4, 6);
    if (part === "name") return name;
    if (part === "year") return yyyymm.slice(0, 4);
    return name + " " + yyyymm.slice(0, 4);
  }
  function niceMax(n) {
    if (n <= 0) return 10;
    var pad = Math.ceil(n * 1.15);
    var mag = Math.pow(10, Math.floor(Math.log(pad) / Math.LN10));
    var nrm = pad / mag;
    var nice = nrm <= 1 ? 1 : nrm <= 2 ? 2 : nrm <= 2.5 ? 2.5 : nrm <= 5 ? 5 : 10;
    return nice * mag;
  }
  function svgEl(name, attrs) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", name);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (attrs[k] !== undefined && attrs[k] !== null) el.setAttribute(k, attrs[k]);
      });
    }
    return el;
  }

  function renderMonthlyChart(qsos) {
    var wrap = document.getElementById("qso-monthly");
    var title = document.getElementById("qso-monthly-title");
    var legendEl = document.getElementById("qso-monthly-legend");
    var chartEl = document.getElementById("qso-monthly-chart");
    var tip = document.getElementById("qso-monthly-tooltip");
    if (!wrap || !title || !legendEl || !chartEl) return;

    var first = "";
    var last = "";
    qsos.forEach(function (q) {
      var d = yyyymmFromDateStr(q.date);
      if (d.length !== 6) return;
      if (!first || d < first) first = d;
      if (!last || d > last) last = d;
    });
    if (!first) {
      wrap.hidden = true;
      monthlyState = null;
      return;
    }
    var nowMonth = yyyymmFromDate(new Date());
    var end = last > nowMonth ? last : nowMonth;
    var months = monthList(first, end);
    var counts = {};
    var used = {};
    months.forEach(function (m) { counts[m] = {}; });
    qsos.forEach(function (q) {
      var m = yyyymmFromDateStr(q.date);
      if (!counts[m]) return;
      var b = q.band || "?";
      counts[m][b] = (counts[m][b] || 0) + 1;
      used[b] = true;
    });
    var bands = BAND_ORDER.filter(function (b) { return used[b]; });
    Object.keys(used).forEach(function (b) {
      if (bands.indexOf(b) < 0) bands.push(b);
    });
    var totals = {};
    var maxTotal = 0;
    months.forEach(function (m) {
      var n = 0;
      bands.forEach(function (b) { n += counts[m][b] || 0; });
      totals[m] = n;
      if (n > maxTotal) maxTotal = n;
    });

    monthlyState = {
      wrap: wrap, title: title, legendEl: legendEl, chartEl: chartEl, tip: tip,
      months: months, bands: bands, counts: counts, totals: totals, maxTotal: maxTotal
    };
    wrap.hidden = false;
    drawMonthlyChart();
    if (!renderMonthlyChart.bound) {
      renderMonthlyChart.bound = true;
      var host = chartEl.parentElement || chartEl;
      if (typeof ResizeObserver === "function") {
        new ResizeObserver(function () { drawMonthlyChart(); }).observe(host);
      } else {
        window.addEventListener("resize", function () { drawMonthlyChart(); });
      }
    }
  }

  function drawMonthlyChart() {
    var s = monthlyState;
    if (!s || s.wrap.hidden) return;
    var t = t10n();
    var lang = (document.documentElement.lang || "sv").slice(0, 2);
    var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]; }); };
    s.title.textContent = t.perMonth;
    s.legendEl.innerHTML = s.bands.map(function (b) {
      return '<span class="qso-monthly-legend-item"><span class="qso-monthly-swatch" style="background:' +
        colorFor(b) + '"></span><span>' + esc(b) + "</span></span>";
    }).join("");

    var yMax = niceMax(s.maxTotal);
    var plotH = 200;
    var padT = 22;
    var padR = 8;
    var padB = 38;
    var padL = 34;
    var host = s.chartEl.parentElement || s.chartEl;
    var avail = host.clientWidth || 600;
    var inner = Math.max(200, avail - padL - padR);
    var minSlot = 28;
    var slot = Math.max(minSlot, inner / Math.max(1, s.months.length));
    var width = padL + padR + slot * s.months.length;
    var barW = Math.max(20, Math.min(64, slot * 0.62));
    var height = padT + plotH + padB;
    var yScale = function (n) { return plotH * (n / yMax); };

    var svg = svgEl("svg", {
      viewBox: "0 0 " + width + " " + height,
      width: String(width),
      height: String(height),
      role: "img",
      "aria-labelledby": "qso-monthly-title"
    });

    var ticks = 4;
    var g;
    for (g = 0; g <= ticks; g++) {
      var val = yMax * (ticks - g) / ticks;
      var y = padT + (plotH * g / ticks);
      var grid = svgEl("line", {
        class: g === ticks ? "qso-monthly-axis" : "qso-monthly-grid",
        x1: String(padL), y1: String(y),
        x2: String(width - padR), y2: String(y)
      });
      svg.appendChild(grid);
      var lab = svgEl("text", {
        class: "qso-monthly-muted",
        x: String(padL - 6), y: String(y + 3.5),
        "text-anchor": "end"
      });
      lab.textContent = String(Math.round(val));
      svg.appendChild(lab);
    }

    function hideTip() {
      if (s.tip) s.tip.style.display = "none";
    }
    function showTip(ev, html) {
      if (!s.tip) return;
      s.tip.innerHTML = html;
      s.tip.style.display = "block";
      moveTip(ev);
    }
    function moveTip(ev) {
      if (!s.tip) return;
      var r = s.wrap.getBoundingClientRect();
      var x = ev.clientX - r.left;
      var y = ev.clientY - r.top;
      var maxX = r.width - 8;
      if (x < 8) x = 8;
      if (x > maxX) x = maxX;
      s.tip.style.left = x + "px";
      s.tip.style.top = y + "px";
    }

    s.months.forEach(function (m, i) {
      var cx = padL + i * slot + slot / 2;
      var x = cx - barW / 2;
      var total = s.totals[m];
      var yCursor = padT + plotH;
      var barGroup = svgEl("g", { "data-month": m });

      if (total === 0) {
        var stub = svgEl("rect", {
          x: String(x), y: String(padT + plotH - 2),
          width: String(barW), height: "2",
          rx: "1",
          fill: "rgba(148,163,184,0.45)",
          "aria-label": monthLabel(m, lang) + ": 0"
        });
        barGroup.appendChild(stub);
      } else {
        s.bands.forEach(function (b) {
          var n = s.counts[m][b] || 0;
          if (!n) return;
          var h = yScale(n);
          yCursor -= h;
          var rect = svgEl("rect", {
            class: "qso-monthly-seg",
            x: String(x),
            y: String(yCursor),
            width: String(barW),
            height: String(Math.max(h, 0.5)),
            fill: colorFor(b),
            tabindex: "0",
            "aria-label": monthLabel(m, lang) + ", " + b + ": " + n + ", " + total + " " + t.monthTotal
          });
          var tipHtml = "<strong>" + esc(monthLabel(m, lang)) + "</strong><br>" +
            esc(b) + ": " + n + "<br>" + total + " " + esc(t.monthTotal);
          rect.addEventListener("mouseenter", function (ev) { showTip(ev, tipHtml); });
          rect.addEventListener("mousemove", moveTip);
          rect.addEventListener("mouseleave", hideTip);
          rect.addEventListener("focus", function (ev) {
            var br = ev.target.getBoundingClientRect();
            showTip({ clientX: br.left + br.width / 2, clientY: br.top }, tipHtml);
          });
          rect.addEventListener("blur", hideTip);
          barGroup.appendChild(rect);
        });
      }

      var totalText = svgEl("text", {
        class: "qso-monthly-total",
        x: String(cx),
        y: String(Math.max(12, yCursor - 5)),
        "text-anchor": "middle"
      });
      totalText.textContent = String(total);
      barGroup.appendChild(totalText);

      var nameText = svgEl("text", {
        class: "qso-monthly-muted",
        x: String(cx),
        y: String(padT + plotH + 14),
        "text-anchor": "middle"
      });
      nameText.textContent = monthLabel(m, lang, "name");
      barGroup.appendChild(nameText);
      var yearText = svgEl("text", {
        class: "qso-monthly-muted",
        x: String(cx),
        y: String(padT + plotH + 27),
        "text-anchor": "middle"
      });
      yearText.textContent = monthLabel(m, lang, "year");
      barGroup.appendChild(yearText);

      svg.appendChild(barGroup);
    });

    s.chartEl.innerHTML = "";
    s.chartEl.appendChild(svg);
  }

})();
