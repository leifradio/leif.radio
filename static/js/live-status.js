(function () {
  "use strict";

  // Capture Leaflet now, before Blowfish's deferred head scripts overwrite window.L.
  var Leaflet = window.L;
  var QRV_SECONDS = 30 * 60;
  var REFRESH_MS = 15 * 60 * 1000;
  var FETCH_TIMEOUT_MS = 15000;
  var CALL = "SM4T";
  var WINDOW_HOURS = 24;
  // Public RBN redistributor with Access-Control-Allow-Origin: *. The path
  // looks exact, but it is a prefix match (SM4TIW is included), so every
  // row is filtered with isOurCall() before use. No tokens.
  var VAIL_URL = "https://vailrerbn.com/api/v1/spots/SM4T?hours=24";
  var BAND_COLORS = {
    "160m": "#7c3aed", "80m": "#2563eb", "60m": "#0891b2", "40m": "#059669",
    "30m": "#65a30d", "20m": "#ca8a04", "17m": "#ea580c", "15m": "#dc2626",
    "12m": "#db2777", "10m": "#c026d3", "6m": "#4f46e5", "2m": "#0ea5e9"
  };
  var FALLBACK = "#64748b";
  var PSK_COLOR = "#0ea5e9";
  var BAND_EDGES = [
    ["160m", 1800, 2000], ["80m", 3500, 4000], ["60m", 5351, 5450],
    ["40m", 7000, 7300], ["30m", 10100, 10150], ["20m", 14000, 14350],
    ["17m", 18068, 18168], ["15m", 21000, 21450], ["12m", 24890, 24990],
    ["10m", 28000, 29700], ["6m", 50000, 54000], ["4m", 70000, 70500],
    ["2m", 144000, 148000]
  ];
  var COUNTRY_SV = {
    "Canary Is.": "Kanarieöarna", "Canary Islands": "Kanarieöarna",
    "Asiatic Russia": "Asiatiska Ryssland", "European Russia": "Europeiska Ryssland",
    "England": "England", "Scotland": "Skottland", "Wales": "Wales",
    "Ireland": "Irland", "Northern Ireland": "Nordirland", "Germany": "Tyskland",
    "France": "Frankrike", "Spain": "Spanien", "Italy": "Italien",
    "Sweden": "Sverige", "Norway": "Norge", "Denmark": "Danmark",
    "Finland": "Finland", "Poland": "Polen", "Netherlands": "Nederländerna",
    "Belgium": "Belgien", "Austria": "Österrike", "Switzerland": "Schweiz",
    "Czech Republic": "Tjeckien", "Slovak Republic": "Slovakien",
    "Hungary": "Ungern", "Romania": "Rumänien", "Bulgaria": "Bulgarien",
    "Greece": "Grekland", "Portugal": "Portugal", "Ukraine": "Ukraina",
    "Belarus": "Belarus", "Lithuania": "Litauen", "Latvia": "Lettland",
    "Estonia": "Estland", "Iceland": "Island", "United States": "USA",
    "Canada": "Kanada", "Japan": "Japan", "China": "Kina",
    "Australia": "Australien", "New Zealand": "Nya Zeeland",
    "South Africa": "Sydafrika", "Brazil": "Brasilien", "Argentina": "Argentina",
    "Turkey": "Turkiet", "Croatia": "Kroatien", "Slovenia": "Slovenien",
    "Serbia": "Serbien", "Bosnia and Herzegovina": "Bosnien och Hercegovina",
    "Faroe Islands": "Färöarna", "Svalbard": "Svalbard",
    "Aland Islands": "Åland", "Luxembourg": "Luxemburg"
  };
  var i18n = {
    sv: {
      home: "QTH", spots: "spots", spot: "spot", reports: "rapporter", report: "rapport",
      title: "SM4T – senaste dygnet",
      lastHeard: "Hörd senast %s på %s %s (RBN, %s, %s dB)",
      lastHeardNoSnr: "Hörd senast %s på %s %s (RBN, %s)",
      noSpots: "Inga RBN-spots det senaste dygnet.",
      rbnUnavailable: "RBN: ingen data",
      rbnSpots: "%s RBN-spots: %s",
      farthest: "Längst bort: %s, %s km",
      pskReports: "PSKReporter: %s %s",
      conditions: "Konditioner: solflöde %s, K-index %s",
      updated: "Uppdaterad %s",
      noData: "Ingen data"
    },
    en: {
      home: "QTH", spots: "spots", spot: "spot", reports: "reports", report: "report",
      title: "SM4T – last 24 hours",
      lastHeard: "Last heard %s on %s %s (RBN, %s, %s dB)",
      lastHeardNoSnr: "Last heard %s on %s %s (RBN, %s)",
      noSpots: "No RBN spots in the last 24 hours.",
      rbnUnavailable: "RBN: no data",
      rbnSpots: "%s RBN spots: %s",
      farthest: "Most distant: %s, %s km",
      pskReports: "PSKReporter: %s %s",
      conditions: "Conditions: solar flux %s, K-index %s",
      updated: "Updated %s",
      noData: "No data"
    }
  };

  var mapInstance = null;
  var currentData = null;

  function lang() {
    return (document.documentElement.lang || "sv").slice(0, 2);
  }
  function t(key) {
    return (i18n[lang()] || i18n.en)[key] || key;
  }
  function fmt(str) {
    var args = Array.prototype.slice.call(arguments, 1);
    var i = 0;
    return String(str).replace(/%s/g, function () {
      var v = args[i++];
      return v == null ? "" : String(v);
    });
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
  function isOurCall(dx) {
    var call = String(dx || "").trim().toUpperCase();
    return call === CALL || call.indexOf(CALL + "/") === 0;
  }
  function normSpotter(call) {
    return String(call || "").trim().toUpperCase().replace(/-\d+$/, "");
  }
  function bandFromFreq(freq) {
    if (freq == null || freq === "") return "";
    var khz = Number(freq);
    if (!isFinite(khz)) return "";
    for (var i = 0; i < BAND_EDGES.length; i++) {
      if (khz >= BAND_EDGES[i][1] && khz <= BAND_EDGES[i][2]) return BAND_EDGES[i][0];
    }
    return "";
  }
  function fmtKm(km) {
    return Number(km).toLocaleString(lang() === "sv" ? "sv-SE" : "en-GB", { maximumFractionDigits: 0 });
  }
  function fmtTime(iso, updatedIso) {
    if (!iso) return "";
    var tDate = new Date(iso);
    if (isNaN(tDate.getTime())) return iso;
    var hh = String(tDate.getUTCHours()).padStart(2, "0");
    var mm = String(tDate.getUTCMinutes()).padStart(2, "0");
    var clock = hh + ":" + mm + " UTC";
    if (updatedIso) {
      var uDate = new Date(updatedIso);
      if (!isNaN(uDate.getTime())) {
        var same = tDate.getUTCFullYear() === uDate.getUTCFullYear() &&
          tDate.getUTCMonth() === uDate.getUTCMonth() &&
          tDate.getUTCDate() === uDate.getUTCDate();
        if (same) return clock;
      }
    }
    var y = tDate.getUTCFullYear();
    var mo = String(tDate.getUTCMonth() + 1).padStart(2, "0");
    var d = String(tDate.getUTCDate()).padStart(2, "0");
    return y + "-" + mo + "-" + d + " " + clock;
  }
  function isoFromEpoch(epoch) {
    return new Date(Number(epoch) * 1000).toISOString().replace(/\.\d{3}Z$/, "Z");
  }
  function haversineKm(lat1, lon1, lat2, lon2) {
    var r = 6371;
    var p1 = lat1 * Math.PI / 180, p2 = lat2 * Math.PI / 180;
    var dphi = (lat2 - lat1) * Math.PI / 180;
    var dlmb = (lon2 - lon1) * Math.PI / 180;
    var a = Math.sin(dphi / 2) * Math.sin(dphi / 2) +
      Math.cos(p1) * Math.cos(p2) * Math.sin(dlmb / 2) * Math.sin(dlmb / 2);
    return r * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }
  function locatorToLatLon(locator) {
    var loc = String(locator || "").trim().toUpperCase();
    if (loc.length < 4) return null;
    if (!/^[A-R][A-R][0-9][0-9]/.test(loc)) return null;
    var lon = (loc.charCodeAt(0) - 65) * 20 - 180;
    var lat = (loc.charCodeAt(1) - 65) * 10 - 90;
    lon += parseInt(loc.charAt(2), 10) * 2;
    lat += parseInt(loc.charAt(3), 10) * 1;
    if (loc.length >= 6 && /[A-X][A-X]/.test(loc.slice(4, 6))) {
      lon += (loc.charCodeAt(4) - 65 + 0.5) * (2 / 24);
      lat += (loc.charCodeAt(5) - 65 + 0.5) * (1 / 24);
    } else {
      lon += 1;
      lat += 0.5;
    }
    return { lat: lat, lon: lon };
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

  function setHidden(el, hidden) {
    if (!el) return;
    el.hidden = !!hidden;
    el.classList.toggle("is-hidden", !!hidden);
  }

  function refreshQrv(data) {
    var badge = document.getElementById("live-status-qrv");
    if (!badge) return;
    var epoch = lastHeardEpoch(data);
    var now = Math.floor(Date.now() / 1000);
    setHidden(badge, !(epoch > 0 && (now - epoch) <= QRV_SECONDS));
  }

  function parseIsoEpoch(value) {
    if (!value) return 0;
    var ms = Date.parse(value);
    return isNaN(ms) ? 0 : Math.floor(ms / 1000);
  }

  function spotKey(spot) {
    var freq = spot.freq == null || spot.freq === "" ? "" : String(Math.round(Number(spot.freq)));
    var epoch = Number(spot.epoch || 0);
    return normSpotter(spot.spotter) + "|" +
      String(spot.dx || CALL).toUpperCase() + "|" + freq + "|" + Math.floor(epoch / 120);
  }
  function spotRank(spot, official) {
    return [Number(spot.epoch || 0), official ? 2 : 1, Number(spot.snr == null ? -99 : spot.snr)];
  }
  function rankGreater(a, b) {
    for (var i = 0; i < 3; i++) {
      if (a[i] > b[i]) return true;
      if (a[i] < b[i]) return false;
    }
    return false;
  }

  function rebuildRbn(base, liveSpots) {
    var cutoff = Math.floor(Date.now() / 1000) - WINDOW_HOURS * 3600;
    var chosen = {};
    var ranks = {};
    function consider(spot, official) {
      if (!spot || !isOurCall(spot.dx || CALL)) return;
      var epoch = Number(spot.epoch || 0);
      if (!epoch || epoch < cutoff) return;
      var key = spotKey(spot);
      var rank = spotRank(spot, official);
      if (!chosen[key] || rankGreater(rank, ranks[key])) {
        chosen[key] = {
          spotter: spot.spotter || "",
          dx: spot.dx || CALL,
          band: spot.band || bandFromFreq(spot.freq),
          mode: (spot.mode || "").toUpperCase(),
          snr: spot.snr == null ? null : Number(spot.snr),
          freq: spot.freq == null ? null : Number(spot.freq),
          epoch: epoch
        };
        ranks[key] = rank;
      }
    }
    (base.spots || []).forEach(function (s) { consider(s, true); });
    (liveSpots || []).forEach(function (s) { consider(s, false); });

    var spots = Object.keys(chosen).map(function (k) { return chosen[k]; });
    spots.sort(function (a, b) {
      return (a.epoch - b.epoch) || ((a.snr || -99) - (b.snr || -99));
    });

    var byBandMap = {};
    var skimmerInfo = {};
    (base.skimmers || []).forEach(function (s) {
      if (s && s.call) skimmerInfo[String(s.call).toUpperCase()] = s;
    });
    var skimmers = {};
    var home = currentData && currentData.home ? currentData.home : { lat: 60.5208, lon: 15.4583, grid: "JP70RM" };

    spots.forEach(function (spot) {
      if (spot.band) byBandMap[spot.band] = (byBandMap[spot.band] || 0) + 1;
      var call = (spot.spotter || "").trim();
      if (!call) return;
      var info = skimmerInfo[call.toUpperCase()] || {};
      var lat = typeof info.lat === "number" ? info.lat : null;
      var lon = typeof info.lon === "number" ? info.lon : null;
      var km = (lat != null && lon != null && home) ? Math.round(haversineKm(home.lat, home.lon, lat, lon)) : null;
      if (!skimmers[call.toUpperCase()]) {
        skimmers[call.toUpperCase()] = {
          call: call,
          country: info.country || "",
          lat: lat,
          lon: lon,
          grid: info.grid || "",
          km: km,
          count: 0,
          lastBand: "",
          lastSnr: null,
          lastEpoch: 0
        };
      }
      var slot = skimmers[call.toUpperCase()];
      slot.count += 1;
      if (spot.epoch >= (slot.lastEpoch || 0)) {
        slot.lastBand = spot.band || "";
        slot.lastSnr = spot.snr;
        slot.lastEpoch = spot.epoch;
      }
    });

    var last = spots.length ? spots[spots.length - 1] : null;
    var lastHeard = null;
    if (last) {
      lastHeard = {
        time: isoFromEpoch(last.epoch),
        epoch: last.epoch,
        band: last.band || "",
        mode: last.mode || "",
        spotter: last.spotter || "",
        snr: last.snr,
        freq: last.freq
      };
    }

    var byBand = BAND_EDGES
      .map(function (row) { return row[0]; })
      .filter(function (b) { return byBandMap[b]; })
      .map(function (b) { return { band: b, count: byBandMap[b] }; });

    var skimmerList = Object.keys(skimmers).map(function (k) { return skimmers[k]; });
    skimmerList.sort(function (a, b) {
      return ((b.km == null ? -1 : b.km) - (a.km == null ? -1 : a.km)) || a.call.localeCompare(b.call);
    });
    var farthest = null;
    var withKm = skimmerList.filter(function (s) { return s.km != null; });
    if (withKm.length) {
      var far = withKm[0];
      farthest = {
        spotter: far.call,
        km: far.km,
        country: far.country || "",
        band: far.lastBand || "",
        snr: far.lastSnr,
        time: far.lastEpoch ? isoFromEpoch(far.lastEpoch) : null
      };
    }

    return {
      ok: true,
      spotCount: spots.length,
      byBand: byBand,
      lastHeard: lastHeard,
      farthest: farthest,
      skimmers: skimmerList,
      spots: spots,
      sources: (base.sources || []).concat(["vailrerbn"]),
      limited: !!base.limited
    };
  }

  function render(data) {
    currentData = data;
    var empty = document.getElementById("live-status-empty");
    var body = document.getElementById("live-status-body");
    var lastEl = document.getElementById("live-status-last");
    var spotsEl = document.getElementById("live-status-spots");
    var farEl = document.getElementById("live-status-farthest");
    var pskEl = document.getElementById("live-status-psk");
    var solarEl = document.getElementById("live-status-solar");
    var updEl = document.getElementById("live-status-updated");
    var hasRbn = data && data.rbn && data.rbn.ok;
    var hasPsk = data && data.psk && data.psk.ok;
    var hasSolar = data && data.solar && data.solar.ok;
    var hasAnything = !!(data && (data.ok || hasRbn || hasPsk || hasSolar));

    if (empty) setHidden(empty, hasAnything);
    if (body) setHidden(body, !hasAnything);
    if (!hasAnything) {
      if (empty) empty.textContent = t("noData");
      refreshQrv(data);
      return;
    }

    if (!hasRbn) {
      if (lastEl) { lastEl.textContent = t("rbnUnavailable"); setHidden(lastEl, false); }
      if (spotsEl) setHidden(spotsEl, true);
      if (farEl) setHidden(farEl, true);
    } else if (!data.rbn.spotCount) {
      if (lastEl) { lastEl.textContent = t("noSpots"); setHidden(lastEl, false); }
      if (spotsEl) setHidden(spotsEl, true);
      if (farEl) setHidden(farEl, true);
    } else {
      var last = data.rbn.lastHeard;
      if (lastEl) {
        if (last) {
          var when = fmtTime(last.time, data.updated);
          var band = bandLabel(last.band);
          if (last.snr != null) {
            lastEl.textContent = fmt(t("lastHeard"), when, band, last.mode, last.spotter, String(last.snr));
          } else {
            lastEl.textContent = fmt(t("lastHeardNoSnr"), when, band, last.mode, last.spotter);
          }
          setHidden(lastEl, false);
        } else {
          setHidden(lastEl, true);
        }
      }
      if (spotsEl) {
        var bits = (data.rbn.byBand || []).map(function (row) {
          return bandLabel(row.band) + " " + row.count;
        });
        spotsEl.textContent = fmt(t("rbnSpots"), String(data.rbn.spotCount), bits.join(", "));
        setHidden(spotsEl, false);
      }
      if (farEl) {
        if (data.rbn.farthest && data.rbn.farthest.spotter != null && data.rbn.farthest.km != null) {
          farEl.textContent = fmt(t("farthest"), data.rbn.farthest.spotter, fmtKm(data.rbn.farthest.km));
          setHidden(farEl, false);
        } else {
          setHidden(farEl, true);
        }
      }
    }

    if (pskEl) {
      var pskCount = hasPsk ? Number(data.psk.reportCount || 0) : 0;
      if (pskCount > 0) {
        var word = pskCount === 1 ? t("report") : t("reports");
        pskEl.textContent = fmt(t("pskReports"), String(pskCount), word);
        setHidden(pskEl, false);
      } else {
        setHidden(pskEl, true);
      }
    }

    if (solarEl) {
      if (hasSolar && (data.solar.sfi != null || data.solar.kIndex != null)) {
        var sfi = data.solar.sfi != null ? String(data.solar.sfi) : "–";
        var k = data.solar.kIndex != null ? String(data.solar.kIndex) : "–";
        solarEl.textContent = fmt(t("conditions"), sfi, k);
        setHidden(solarEl, false);
      } else {
        setHidden(solarEl, true);
      }
    }

    if (updEl && data.updated) {
      updEl.textContent = fmt(t("updated"), fmtTime(data.updated, data.updated));
    }

    refreshQrv(data);
    initMap(data);
  }

  function initMap(data) {
    var holder = document.getElementById("live-status-map");
    if (!holder) return;
    var points = [];
    var rbn = (data.rbn && data.rbn.ok && data.rbn.skimmers) || [];
    rbn.forEach(function (s) {
      if (typeof s.lat === "number" && typeof s.lon === "number") points.push({ kind: "rbn", s: s });
    });
    var psk = (data.psk && data.psk.ok && data.psk.receivers) || [];
    psk.forEach(function (s) {
      if (typeof s.lat === "number" && typeof s.lon === "number") points.push({ kind: "psk", s: s });
    });
    if (!points.length || !Leaflet || !Leaflet.version || typeof Leaflet.map !== "function" || Leaflet.map === Array.prototype.map) {
      if (mapInstance) {
        mapInstance.remove();
        mapInstance = null;
      }
      holder.style.display = points.length ? holder.style.display : "none";
      if (!points.length) holder.hidden = true;
      return;
    }
    holder.hidden = false;
    holder.style.display = "";
    if (mapInstance) {
      mapInstance.remove();
      mapInstance = null;
      holder.innerHTML = "";
    }

    var map = Leaflet.map(holder, { scrollWheelZoom: false, attributionControl: true });
    mapInstance = map;
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
      if (s.km != null) bits.push(fmtKm(s.km) + " km");
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

  function fetchJson(url, timeoutMs) {
    var ctrl = typeof AbortController === "function" ? new AbortController() : null;
    var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, timeoutMs || FETCH_TIMEOUT_MS) : null;
    return fetch(url, {
      method: "GET",
      cache: "no-store",
      signal: ctrl ? ctrl.signal : undefined,
      headers: { "Accept": "application/json" }
    }).then(function (resp) {
      if (!resp.ok) throw new Error("HTTP " + resp.status);
      return resp.json();
    }).finally(function () {
      if (timer) clearTimeout(timer);
    });
  }

  function vailToSpots(payload) {
    var rows = (payload && payload.spots) || [];
    var out = [];
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      if (!row || !isOurCall(row.callsign)) continue;
      var epoch = parseIsoEpoch(row.timestamp);
      if (!epoch) continue;
      var freq = row.frequency == null ? null : Number(row.frequency);
      out.push({
        spotter: row.spotter || "",
        dx: row.callsign || "",
        band: bandFromFreq(freq),
        mode: (row.mode || "").toUpperCase(),
        snr: row.snr == null ? null : Number(row.snr),
        freq: freq,
        epoch: epoch,
        grid: row.spotter_grid || ""
      });
      if (row.spotter_grid && currentData) {
        var call = String(row.spotter || "").toUpperCase();
        var coords = locatorToLatLon(row.spotter_grid);
        if (call && coords && currentData.rbn && currentData.rbn.skimmers) {
          var found = currentData.rbn.skimmers.some(function (s) {
            return String(s.call || "").toUpperCase() === call;
          });
          if (!found) {
            currentData.rbn.skimmers.push({
              call: row.spotter,
              lat: coords.lat,
              lon: coords.lon,
              grid: row.spotter_grid,
              country: "",
              count: 0
            });
          }
        }
      }
    }
    return out;
  }

  function refreshFromVail() {
    if (!currentData) return Promise.resolve();
    return fetchJson(VAIL_URL, FETCH_TIMEOUT_MS).then(function (payload) {
      var liveSpots = vailToSpots(payload);
      if (!liveSpots.length && !(currentData.rbn && currentData.rbn.spots && currentData.rbn.spots.length)) {
        return;
      }
      var base = currentData.rbn && currentData.rbn.ok ? currentData.rbn : { spots: [], skimmers: [], sources: [] };
      var rbn = rebuildRbn(base, liveSpots);
      var next = {};
      Object.keys(currentData).forEach(function (k) { next[k] = currentData[k]; });
      next.rbn = rbn;
      next.ok = true;
      next.updated = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
      next.qrv = !!(rbn.lastHeard && (Math.floor(Date.now() / 1000) - rbn.lastHeard.epoch) <= QRV_SECONDS);
      render(next);
    }).catch(function () {
      // Keep the baked (or last good) data if the live source is down.
    });
  }

  var data = readData();
  if (!data) return;
  currentData = data;
  function start() {
    render(data);
    refreshFromVail();
    setInterval(refreshFromVail, REFRESH_MS);
    setInterval(function () { refreshQrv(currentData); }, 60000);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
