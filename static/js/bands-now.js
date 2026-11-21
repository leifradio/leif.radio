(function () {
  "use strict";
  // Renders the "Band openings right now" grid from /data/bands-now.json.
  var URL_JSON = "/data/bands-now.json";
  var REFRESH_MS = 5 * 60 * 1000;   // re-read the json (the build updates it ~every 15–60 min)
  var STALE_MIN = 75;               // warn when older than this
  var DEAD_MIN = 6 * 60;            // treat as missing when older than this
  var CONTS = ["EU", "NA", "SA", "AF", "AS", "OC"];

  var root = document.getElementById("bands-now");
  if (!root) return;
  var T = {};
  try { T = JSON.parse(document.getElementById("bands-now-i18n").textContent); } catch (e) {}
  var $ = function (id) { return document.getElementById(id); };
  var fmt = function (s) {
    var args = Array.prototype.slice.call(arguments, 1), i = 0;
    return String(s || "").replace(/%s/g, function () { return args[i++]; });
  };
  var num = function (v, d) {
    return new Intl.NumberFormat(T.locale || "sv-SE", { maximumFractionDigits: d }).format(v);
  };

  function level(n, levels) {
    var l = 0;
    for (var i = 0; i < levels.length; i++) if (n >= levels[i]) l = i + 1;
    return l;
  }

  function stockholm(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return "";
    var opts = { timeZone: "Europe/Stockholm", hour: "2-digit", minute: "2-digit" };
    var today = new Date().toLocaleDateString("sv-SE", { timeZone: "Europe/Stockholm" });
    var day = d.toLocaleDateString("sv-SE", { timeZone: "Europe/Stockholm" });
    var s = d.toLocaleTimeString(T.locale || "sv-SE", opts);
    if (day !== today) s = d.toLocaleDateString(T.locale || "sv-SE", { timeZone: "Europe/Stockholm", day: "numeric", month: "short" }) + " " + s;
    return s + " (" + T.tz + ")";
  }

  function status(text) {
    var el = $("bands-now-status");
    el.textContent = text || "";
    el.hidden = !text;
  }

  function render(d) {
    var grid = $("bands-now-grid");
    var age = d && d.updated ? (Date.now() - new Date(d.updated).getTime()) / 60000 : Infinity;
    var usable = d && d.ok && Array.isArray(d.bands) && age < DEAD_MIN;

    $("bands-now-updated").textContent = d && d.updated ? fmt(T.updated, stockholm(d.updated)) + ". " : "";

    if (d && d.solar && d.solar.ok) {
      var kp = d.solar.kp != null ? num(d.solar.kp, 1) : "–";
      var sfi = d.solar.sfi != null ? String(d.solar.sfi) : "–";
      $("bands-now-solar").textContent = fmt(T.solar, kp, sfi);
      $("bands-now-solar").hidden = false;
    }

    if (!usable) {
      grid.hidden = true;
      status(d && d.updated && isFinite(age) && age >= DEAD_MIN ? T.noData + " " + fmt(T.stale, Math.floor(age)) : T.noData);
      $("bands-now-skimmers").textContent = "";
      return;
    }
    status(age > STALE_MIN ? fmt(T.stale, Math.floor(age)) : "");

    var levels = d.levels || [1, 3, 10];
    var conts = d.continents || CONTS;
    var head = "<tr><th scope=\"col\">" + T.band + "</th>";
    conts.forEach(function (c) {
      head += "<th scope=\"col\"><abbr title=\"" + (T["cont" + c] || c) + "\">" + c + "</abbr></th>";
    });
    grid.tHead.innerHTML = head + "</tr>";

    var body = "";
    d.bands.forEach(function (b) {
      var label = String(b.band).replace("m", " m");
      body += "<tr><th scope=\"row\">" + label + "</th>";
      conts.forEach(function (c) {
        var n = (b.cells && b.cells[c]) || 0;
        var capped = (b.capped || []).indexOf(c) >= 0;
        var shown = n ? (capped ? "≥" + n : String(n)) : "";
        var title = fmt(T.cellTitle, label, T["cont" + c] || c, (capped ? T.capped + " " : "") + n);
        body += "<td class=\"bn-l" + level(n, levels) + "\" title=\"" + title + "\"><span class=\"sr-only\">" + title + "</span><span aria-hidden=\"true\">" + shown + "</span></td>";
      });
      body += "</tr>";
    });
    grid.tBodies[0].innerHTML = body;
    grid.hidden = false;

    var sk = (d.skimmers || []).filter(function (s) { return s.spots == null || s.spots > 0; }).map(function (s) { return s.call + " (" + s.km + " km)"; });
    $("bands-now-skimmers").textContent = sk.length ? fmt(T.skimmers, sk.join(", ")) + " " : "";
  }

  function load() {
    fetch(URL_JSON + "?t=" + Math.floor(Date.now() / 60000), { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(render)
      .catch(function () { render(null); });
  }

  load();
  setInterval(load, REFRESH_MS);
})();
