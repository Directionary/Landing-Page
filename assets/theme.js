/* Theme switching. Loaded synchronously in <head> so the resolved theme is applied
   before first paint. Priority: stored choice in localStorage, else the OS /
   browser preference via prefers-color-scheme (auto-detect). The toggle is a
   button whose accessible name describes the action it will perform
   ("Switch to dark mode" / "Switch to light mode"). When no stored choice
   exists, system changes are followed live. */
(function () {
  var KEY = "directionary-theme";
  var root = document.documentElement;
  var media = (window.matchMedia)
    ? window.matchMedia("(prefers-color-scheme: dark)")
    : null;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function systemTheme() {
    return (media && media.matches) ? "dark" : "light";
  }

  function resolve() {
    var s = stored();
    if (s === "dark" || s === "light") return s;
    return systemTheme();
  }

  function syncMeta(theme) {
    var meta = document.querySelector('meta[name="theme-color"]');
    if (!meta) return;
    meta.setAttribute("content", theme === "dark" ? "#191815" : "#faf9f6");
  }

  function apply(theme) {
    if (theme === "dark") root.setAttribute("data-theme", "dark");
    else root.removeAttribute("data-theme");
    syncMeta(theme);
  }

  apply(resolve());

  // Follow the system while the user has not made an explicit choice.
  if (media) {
    var onSystemChange = function (e) {
      var s = stored();
      if (s !== "dark" && s !== "light") apply(e.matches ? "dark" : "light");
    };
    if (media.addEventListener) media.addEventListener("change", onSystemChange);
    else if (media.addListener) media.addListener(onSystemChange);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var button = document.getElementById("theme-toggle");
    if (!button) return;

    function sync() {
      var dark = root.getAttribute("data-theme") === "dark";
      button.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    }
    sync();

    button.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      apply(next);
      try { localStorage.setItem(KEY, next); } catch (e) {}
      sync();
    });
  });
})();
