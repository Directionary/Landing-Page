/* Theme switching. Loaded synchronously in <head> so the stored theme is applied
   before first paint. Light is the default. The toggle is a button whose name
   stays "Dark mode" and whose state is exposed with aria-pressed. */
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
    var button = document.getElementById("theme-toggle");
    if (!button) return;

    function sync() {
      button.setAttribute("aria-pressed", root.getAttribute("data-theme") === "dark" ? "true" : "false");
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
