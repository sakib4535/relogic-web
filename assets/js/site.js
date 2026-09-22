(function relogicSite() {
  "use strict";

  var rawPath = (window.location.pathname || "/").replace(/\/+$/, "") || "/";
  var path = rawPath.toLowerCase();

  function sectionOf(p) {
    p = String(p || "/").split("#")[0].replace(/\/+$/, "") || "/";
    if (p === "/" || p === "/index") return "home";
    if (p.indexOf("/services") === 0) return "services";
    if (p.indexOf("/research") === 0) return "research";
    if (p.indexOf("/projects") === 0) return "projects";
    if (p.indexOf("/people") === 0) return "people";
    return p.replace(/^\//, "").replace(/\.html$/, "") || "home";
  }
  var section = sectionOf(path);

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
      fn();
    }
  }

  function markActive() {
    document.querySelectorAll(".nav-links a, .mobile-menu a").forEach(function (link) {
      var href = (link.getAttribute("href") || "").split("#")[0] || "/";
      var linkSection = sectionOf(href);
      if (linkSection === section) link.classList.add("active");
    });
  }

  function bindChrome() {
    var shell = document.getElementById("navShell");
    var btn = document.getElementById("menuBtn");
    var menu = document.getElementById("mobileMenu");
    var bar = document.getElementById("scrollProgress");

    if (btn && menu) {
      btn.addEventListener("click", function () {
        var open = menu.classList.toggle("open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
      menu.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () {
          menu.classList.remove("open");
          btn.setAttribute("aria-expanded", "false");
        });
      });
    }

    var onScroll = function () {
      var y = window.scrollY || 0;
      if (shell) shell.classList.toggle("scrolled", y > 8);
      if (bar) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        var pct = max > 0 ? (y / max) * 100 : 0;
        bar.style.width = pct + "%";
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  function hardenLinks() {
    document.querySelectorAll('a[href^="http"]').forEach(function (a) {
      try {
        var url = new URL(a.href, window.location.href);
        if (url.origin !== window.location.origin) {
          a.setAttribute("rel", "noopener noreferrer nofollow");
          if (!a.getAttribute("target")) a.setAttribute("target", "_blank");
        }
      } catch (e) {}
    });
  }

  function reveal() {
    var nodes = document.querySelectorAll(".reveal");
    if (!nodes.length) return;
    if (!("IntersectionObserver" in window)) {
      nodes.forEach(function (n) { n.classList.add("visible"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    nodes.forEach(function (n) { io.observe(n); });
  }

  ready(function () {
    document.body.classList.add("rl-has-chrome");
    markActive();
    hardenLinks();
    // index.html already owns scroll, menu and reveal behaviour
    if (section !== "home") {
      bindChrome();
      reveal();
    }
  });
})();
