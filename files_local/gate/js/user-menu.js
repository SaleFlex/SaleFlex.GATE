(function () {
  "use strict";

  function closeMenu(root) {
    var panel = root.querySelector(".user-menu__panel");
    var trigger = root.querySelector(".user-menu__trigger");
    if (!panel || !trigger) return;
    panel.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
    root.querySelectorAll(".user-menu__sub").forEach(function (sub) {
      sub.hidden = true;
    });
    root.querySelectorAll(".user-menu__sub-toggle").forEach(function (btn) {
      btn.setAttribute("aria-expanded", "false");
    });
  }

  function openMenu(root) {
    var panel = root.querySelector(".user-menu__panel");
    var trigger = root.querySelector(".user-menu__trigger");
    if (!panel || !trigger) return;
    panel.hidden = false;
    trigger.setAttribute("aria-expanded", "true");
  }

  document.querySelectorAll("[data-user-menu]").forEach(function (root) {
    var trigger = root.querySelector(".user-menu__trigger");
    var panel = root.querySelector(".user-menu__panel");

    if (!trigger || !panel) return;

    trigger.addEventListener("click", function () {
      var open = trigger.getAttribute("aria-expanded") === "true";
      document.querySelectorAll("[data-theme-picker]").forEach(function (tp) {
        var pp = tp.querySelector(".theme-picker__panel");
        var tt = tp.querySelector(".theme-picker__trigger");
        if (pp && tt) {
          pp.hidden = true;
          tt.setAttribute("aria-expanded", "false");
        }
      });
      document.querySelectorAll("[data-user-menu]").forEach(function (other) {
        if (other !== root) closeMenu(other);
      });
      if (open) {
        closeMenu(root);
      } else {
        openMenu(root);
      }
    });

    panel.querySelectorAll(".user-menu__sub-toggle").forEach(function (subToggle) {
      var sid = subToggle.getAttribute("aria-controls");
      if (!sid) return;
      var sub = document.getElementById(sid);
      if (!sub || !panel.contains(sub)) return;
      subToggle.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var expanded = subToggle.getAttribute("aria-expanded") === "true";
        if (expanded) {
          sub.querySelectorAll(".user-menu__sub").forEach(function (nest) {
            nest.hidden = true;
          });
          sub.querySelectorAll(".user-menu__sub-toggle").forEach(function (t) {
            if (t !== subToggle) {
              t.setAttribute("aria-expanded", "false");
            }
          });
        }
        sub.hidden = expanded;
        subToggle.setAttribute("aria-expanded", expanded ? "false" : "true");
      });
    });
  });

  document.addEventListener("click", function (e) {
    document.querySelectorAll("[data-user-menu]").forEach(function (root) {
      if (!root.contains(e.target)) {
        closeMenu(root);
      }
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll("[data-user-menu]").forEach(closeMenu);
    }
  });
})();
