/* Theme switching. Loaded synchronously in <head> so the stored theme is
   applied before first paint. Light is the default. The control is a pair of
   native radio buttons, so arrow keys and screen reader semantics come free. */
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
    var radios = document.querySelectorAll('input[name="theme"]');
    var current = root.getAttribute("data-theme") === "dark" ? "dark" : "light";

    Array.prototype.forEach.call(radios, function (radio) {
      radio.checked = radio.value === current;
      radio.addEventListener("change", function () {
        if (!radio.checked) return;
        apply(radio.value);
        try { localStorage.setItem(KEY, radio.value); } catch (e) {}
      });
    });
  });
})();
