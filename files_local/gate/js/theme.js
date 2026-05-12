(function () {
  "use strict";

  var STORAGE_KEY = "saleflex-gate-theme";

  function getPref() {
    try {
      var p = localStorage.getItem(STORAGE_KEY);
      if (p === "light" || p === "dark" || p === "system") return p;
    } catch (e) {}
    return "system";
  }

  function setPref(pref) {
    if (pref !== "light" && pref !== "dark" && pref !== "system") return;
    try {
      localStorage.setItem(STORAGE_KEY, pref);
    } catch (e) {}
  }

  function effective(pref) {
    if (pref === "system") {
      return window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
    }
    return pref;
  }

  var mediaListener = null;

  function updateMetaTheme(eff) {
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute("content", eff === "dark" ? "#0f172a" : "#0f766e");
    }
  }

  function syncPickerUI() {
    var pref = getPref();
    document.querySelectorAll("[data-theme-picker]").forEach(function (root) {
      root.querySelectorAll("[data-theme-value]").forEach(function (btn) {
        var v = btn.getAttribute("data-theme-value");
        var on = v === pref;
        btn.setAttribute("aria-pressed", on ? "true" : "false");
        btn.classList.toggle("is-active", on);
      });
      var trig = root.querySelector(".theme-picker__trigger");
      if (trig) {
        var label =
          pref === "system"
            ? "System"
            : pref.charAt(0).toUpperCase() + pref.slice(1);
        trig.setAttribute("title", "Theme (" + label + ")");
      }
    });
  }

  function applyFromStorage() {
    var pref = getPref();
    var eff = effective(pref);
    document.documentElement.setAttribute("data-theme", eff);
    document.documentElement.setAttribute("data-theme-pref", pref);
    updateMetaTheme(eff);

    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mediaListener) {
      mq.removeEventListener("change", mediaListener);
      mediaListener = null;
    }
    if (pref === "system") {
      mediaListener = function () {
        var e = effective("system");
        document.documentElement.setAttribute("data-theme", e);
        updateMetaTheme(e);
        syncPickerUI();
      };
      mq.addEventListener("change", mediaListener);
    }
    syncPickerUI();
  }

  function closePicker(root) {
    var panel = root.querySelector(".theme-picker__panel");
    var trig = root.querySelector(".theme-picker__trigger");
    if (!panel || !trig) return;
    panel.hidden = true;
    trig.setAttribute("aria-expanded", "false");
  }

  function openPicker(root) {
    var panel = root.querySelector(".theme-picker__panel");
    var trig = root.querySelector(".theme-picker__trigger");
    if (!panel || !trig) return;
    panel.hidden = false;
    trig.setAttribute("aria-expanded", "true");
  }

  function wirePickers() {
    document.querySelectorAll("[data-theme-picker]").forEach(function (root) {
      var trig = root.querySelector(".theme-picker__trigger");
      var panel = root.querySelector(".theme-picker__panel");
      var optionRoot = panel || root;

      optionRoot.querySelectorAll("[data-theme-value]").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          e.stopPropagation();
          var v = btn.getAttribute("data-theme-value");
          if (v === "light" || v === "dark" || v === "system") {
            setPref(v);
            applyFromStorage();
          }
          closePicker(root);
        });
      });

      if (!trig || !panel) return;

      trig.addEventListener("click", function (e) {
        e.stopPropagation();
        var open = trig.getAttribute("aria-expanded") === "true";
        document.querySelectorAll("[data-theme-picker]").forEach(function (other) {
          if (other !== root) closePicker(other);
        });
        document.querySelectorAll("[data-user-menu]").forEach(function (um) {
          var pt = um.querySelector(".user-menu__panel");
          var tb = um.querySelector(".user-menu__trigger");
          if (pt && tb) {
            pt.hidden = true;
            tb.setAttribute("aria-expanded", "false");
          }
        });
        if (open) closePicker(root);
        else openPicker(root);
      });
    });
  }

  document.addEventListener("click", function (e) {
    document.querySelectorAll("[data-theme-picker]").forEach(function (root) {
      if (!root.contains(e.target)) closePicker(root);
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll("[data-theme-picker]").forEach(closePicker);
    }
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      applyFromStorage();
      wirePickers();
    });
  } else {
    applyFromStorage();
    wirePickers();
  }
})();
