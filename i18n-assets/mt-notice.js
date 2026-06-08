/* hydro-informatics.com — machine-translation notice for DE/FR pages.
 *
 * Injected into every built page (see i18n/inject_i18n.py) but self-gates: it
 * does nothing on English pages and only shows a small dismissible toast on the
 * /de/ and /fr/ trees, telling readers the page was machine-translated and may
 * contain errors, with a link back to the English original.
 *
 * IMPORTANT — same constraints as lang-switcher.js: the book-theme is a Remix
 * app that calls hydrateRoot(document), so React owns the whole document. A node
 * we append to <body> is a hydration mismatch and gets removed, so we re-assert
 * it (MutationObserver + a bounded interval). Remix also strips foreign <head>
 * tags, so the toast is styled with INLINE styles, not a stylesheet.
 *
 * Dismissal is remembered in localStorage, so once a reader closes it the toast
 * does not reappear on subsequent pages.
 */
(function () {
  "use strict";

  var locale = (location.pathname.match(/^\/(de|fr)(?=\/|$)/) || [])[1];
  if (!locale) return; // English (source of truth) — no notice.

  var DISMISS_KEY = "hy-mt-notice-dismissed";
  try { if (localStorage.getItem(DISMISS_KEY) === "1") return; } catch (e) {}

  var TEXT = {
    de: {
      msg: "Diese Seite wurde maschinell aus dem Englischen übersetzt und kann Fehler enthalten.",
      orig: "Original auf Englisch ansehen",
      close: "Hinweis schließen"
    },
    fr: {
      msg: "Cette page a été traduite automatiquement de l’anglais et peut contenir des erreurs.",
      orig: "Voir l’original en anglais",
      close: "Fermer l’avis"
    }
  }[locale];

  function originalHref() {
    var base = location.pathname.slice(3) || "/"; // strip leading "/de" | "/fr"
    if (base.charAt(0) !== "/") base = "/" + base;
    return base + location.search + location.hash;
  }
  function isDark() {
    return document.documentElement.classList.contains("dark");
  }

  var dismissed = false;

  function build() {
    var dark = isDark();
    var box = document.createElement("div");
    box.className = "hy-mt-notice";
    box.setAttribute("role", "status");
    box.style.cssText = [
      "position:fixed",
      "z-index:2147483646",
      "bottom:1rem",
      "left:1rem",
      "right:1rem",
      "max-width:24rem",
      "margin:0 auto",
      "padding:0.85rem 2rem 0.85rem 1rem",
      "border:1px solid " + (dark ? "#57534e" : "#d6d3d1"),
      "border-radius:0.6rem",
      "background-color:" + (dark ? "#1c1917" : "#ffffff"),
      "color:" + (dark ? "#e7e5e4" : "#1c1917"),
      "box-shadow:0 4px 16px rgba(0,0,0,0.18)",
      "font-size:0.82rem",
      "line-height:1.4",
      "font-family:inherit"
    ].join(";");

    var msg = document.createElement("div");
    msg.textContent = TEXT.msg;
    msg.style.cssText = "margin-bottom:0.5rem;";

    var link = document.createElement("a");
    link.href = originalHref();
    link.textContent = TEXT.orig + " →";
    link.style.cssText =
      "color:" + (dark ? "#93c5fd" : "#1d4ed8") +
      ";font-weight:600;text-decoration:underline;";

    var close = document.createElement("button");
    close.type = "button";
    close.setAttribute("aria-label", TEXT.close);
    close.title = TEXT.close;
    close.textContent = "×";
    close.style.cssText = [
      "position:absolute",
      "top:0.3rem",
      "right:0.5rem",
      "border:0",
      "background:transparent",
      "cursor:pointer",
      "font-size:1.3rem",
      "line-height:1",
      "color:" + (dark ? "#a8a29e" : "#78716c")
    ].join(";");
    close.addEventListener("click", function () {
      dismissed = true;
      try { localStorage.setItem(DISMISS_KEY, "1"); } catch (e) {}
      if (box.parentNode) box.parentNode.removeChild(box);
    });

    box.appendChild(close);
    box.appendChild(msg);
    box.appendChild(link);
    return box;
  }

  function ensure() {
    if (dismissed || !document.body) return;
    if (document.querySelector(".hy-mt-notice")) return;
    document.body.appendChild(build());
  }
  function repaint() {
    // Theme toggled: rebuild so dark/light colors track <html>.class.
    var el = document.querySelector(".hy-mt-notice");
    if (el && el.parentNode) { el.parentNode.removeChild(el); ensure(); }
  }

  function watch() {
    ensure();
    if (document.body) {
      new MutationObserver(function () { ensure(); })
        .observe(document.body, { childList: true, subtree: true });
    }
    new MutationObserver(repaint)
      .observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
    var tries = 0;
    var iv = setInterval(function () {
      ensure();
      if (++tries >= 48) clearInterval(iv); // ~12 s, mirrors lang-switcher
    }, 250);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", watch);
  } else {
    watch();
  }
})();
