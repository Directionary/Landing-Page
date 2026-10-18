/* Theme switching. Loaded synchronously in <head> so the stored theme is applied
   before first paint. Light is the default. The control is a native checkbox with
   role="switch" (checked = dark), so state and keyboard support are built in. */
(function () {
  var KEY = "directionary-theme";
  var root = document.documentElement;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function apply(theme) {
    if (theme === "dark") root.setAttribute("data-theme", "dark");
    else root.removeAttribute("data-theme");
  }

  apply(stored() === "dark" ? "dark" : "light");

  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("theme-switch");
    if (!toggle) return;

    toggle.checked = root.getAttribute("data-theme") === "dark";
    toggle.addEventListener("change", function () {
      var theme = toggle.checked ? "dark" : "light";
      apply(theme);
      try { localStorage.setItem(KEY, theme); } catch (e) {}
    });
  });
})();
