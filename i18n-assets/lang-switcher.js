/* hydro-informatics.com — language switcher + browser-language auto-detect.
 *
 * Injected into every built page of all three locales (see i18n/inject_i18n.py).
 * The site is served as three sibling static builds:
 *     /            English   (default + fallback)
 *     /de/...      German    (de, de-CH, de-AT, de-LI, ...)
 *     /fr/...      French    (fr, fr-CH, fr-BE, fr-CA, ...)
 *
 * Loaded synchronously in <head> so the redirect decision runs before paint
 * (no flash of the wrong language).
 *
 * IMPORTANT — the book-theme is a Remix app that calls hydrateRoot(document),
 * so React owns the *entire* document. Two consequences shape this script:
 *   1. Any node we insert into the navbar is a hydration mismatch and gets
 *      removed by React, so we must re-assert it (MutationObserver + a bounded
 *      interval that survives React's async/concurrent hydration window).
 *   2. Remix manages <head> and strips foreign tags, so our stylesheet <link>
 *      cannot be relied upon — the control is styled with INLINE styles instead
 *      (the companion .css file is now only a progressive-enhancement nicety).
 */
(function () {
  "use strict";

  var LOCALES = ["en", "de", "fr"];
  var LABELS = { en: "English", de: "Deutsch", fr: "Français" };
  var SHORT = { en: "EN", de: "DE", fr: "FR" };
  var STORE_KEY = "hy-lang";          // persisted manual/auto choice (localStorage)
  var SESSION_FLAG = "hy-lang-seen";  // per-session guard against redirect loops

  // ---- path helpers -------------------------------------------------------
  function localeOf(path) {
    var m = path.match(/^\/(de|fr)(?=\/|$)/);
    return m ? m[1] : "en";
  }
  function basePath(path) {
    return localeOf(path) === "en" ? path || "/" : path.slice(3) || "/";
  }
  function localize(path, target) {
    var b = basePath(path);
    if (target === "en") return b;
    return "/" + target + (b === "/" ? "/" : b);
  }

  // First browser/system preference -> en | de | fr (defaults to en).
  function detect() {
    var langs = navigator.languages && navigator.languages.length
      ? navigator.languages : [navigator.language || "en"];
    var primary = (langs[0] || "en").toLowerCase();
    if (primary.indexOf("fr") === 0) return "fr";
    if (primary.indexOf("de") === 0) return "de";
    return "en"; // everything else, and any doubt, -> English
  }

  function go(target) {
    var dest = localize(location.pathname, target) + location.search + location.hash;
    location.replace(dest);
  }

  // ---- redirect decision (runs immediately) -------------------------------
  var current = localeOf(location.pathname);
  var stored = null;
  try { stored = localStorage.getItem(STORE_KEY); } catch (e) {}

  if (stored && LOCALES.indexOf(stored) !== -1) {
    // Remembered choice wins on every page; redirect only if not already there.
    if (stored !== current) { go(stored); return; }
  } else {
    var seen = false;
    try { seen = sessionStorage.getItem(SESSION_FLAG) === "1"; } catch (e) {}
    if (!seen) {
      try { sessionStorage.setItem(SESSION_FLAG, "1"); } catch (e) {}
      if (current !== "en") {
        // Landed directly on a locale URL -> treat as intentional, remember it.
        try { localStorage.setItem(STORE_KEY, current); } catch (e) {}
      } else {
        // Plain English URL with no stored preference -> auto-detect once.
        var want = detect();
        try { localStorage.setItem(STORE_KEY, want); } catch (e) {}
        if (want !== "en") { go(want); return; }
      }
    }
  }

  // ---- visible switcher control (inline-styled, React-proof) --------------
  function isDark() {
    return document.documentElement.classList.contains("dark");
  }

  function paint(sel) {
    // Inline styles so the control stays visible even if Remix strips our
    // stylesheet <link>. Mirrors the .myst-theme-button look (rounded, h-10).
    var dark = isDark();
    sel.style.cssText = [
      "appearance:none",
      "-webkit-appearance:none",
      "-moz-appearance:none",
      "height:2.5rem",
      "padding:0 1.6rem 0 0.7rem",
      "margin-left:0.75rem",
      "border:1px solid " + (dark ? "#ffffff" : "#44403c"),
      "border-radius:9999px",
      "background-color:transparent",
      "color:" + (dark ? "#ffffff" : "#44403c"),
      "font-size:0.8rem",
      "font-weight:600",
      "line-height:1",
      "cursor:pointer",
      "background-repeat:no-repeat",
      "background-position:right 0.45rem center",
      "background-size:1rem",
      "background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%23" +
        (dark ? "ffffff" : "78716c") +
        "'%3E%3Cpath fill-rule='evenodd' d='M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z' clip-rule='evenodd'/%3E%3C/svg%3E\")"
    ].join(";");
  }

  function buildControl() {
    var sel = document.createElement("select");
    sel.setAttribute("aria-label", "Select language / Sprache / langue");
    sel.className = "hy-lang-select hy-lang-switcher";
    LOCALES.forEach(function (lc) {
      var opt = document.createElement("option");
      opt.value = lc;
      opt.textContent = SHORT[lc];
      opt.title = LABELS[lc];
      opt.style.color = "#1c1917";
      if (lc === current) opt.selected = true;
      sel.appendChild(opt);
    });
    sel.addEventListener("change", function () {
      var target = sel.value;
      try { localStorage.setItem(STORE_KEY, target); } catch (e) {}
      if (target !== current) go(target);
    });
    paint(sel);
    return sel;
  }

  function repaintIfPresent() {
    var el = document.querySelector(".hy-lang-switcher");
    if (el) paint(el);
  }

  function ensureControl() {
    if (document.querySelector(".hy-lang-switcher")) return true;
    // Anchor next to the theme (dark/light) toggle in the top-right navbar.
    var anchor = document.querySelector(".myst-theme-button");
    if (!anchor || !anchor.parentNode) return false;
    anchor.parentNode.insertBefore(buildControl(), anchor);
    return true;
  }

  function watch() {
    ensureControl();

    // (1) React removes our node during hydration / re-renders -> re-insert.
    if (document.body) {
      new MutationObserver(function () { ensureControl(); })
        .observe(document.body, { childList: true, subtree: true });
    }

    // (2) Repaint when the theme toggles (book-theme flips `dark` on <html>).
    new MutationObserver(repaintIfPresent)
      .observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

    // (3) Bounded interval safety-net: React's async/concurrent hydration can
    //     remove our node in a batch the observer misses on first paint. Keep
    //     re-asserting for ~12 s, then stop (the observer covers later changes).
    var tries = 0;
    var iv = setInterval(function () {
      ensureControl();
      if (++tries >= 48) clearInterval(iv);
    }, 250);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", watch);
  } else {
    watch();
  }
})();
