(function () {
  "use strict";

  function closeMenu(root) {
    var panel = root.querySelector(".user-menu__panel");
    var trigger = root.querySelector(".user-menu__trigger");
    if (!panel || !trigger) return;
    panel.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
    var sub = root.querySelector(".user-menu__sub");
    var subBtn = root.querySelector(".user-menu__sub-toggle");
    if (sub) sub.hidden = true;
    if (subBtn) subBtn.setAttribute("aria-expanded", "false");
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
    var subToggle = root.querySelector(".user-menu__sub-toggle");
    var sub = root.querySelector(".user-menu__sub");

    if (!trigger || !panel) return;

    trigger.addEventListener("click", function () {
      var open = trigger.getAttribute("aria-expanded") === "true";
      document.querySelectorAll("[data-user-menu]").forEach(function (other) {
        if (other !== root) closeMenu(other);
      });
      if (open) {
        closeMenu(root);
      } else {
        openMenu(root);
      }
    });

    if (subToggle && sub) {
      subToggle.addEventListener("click", function (e) {
        e.preventDefault();
        var expanded = subToggle.getAttribute("aria-expanded") === "true";
        sub.hidden = expanded;
        subToggle.setAttribute("aria-expanded", expanded ? "false" : "true");
      });
    }
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
