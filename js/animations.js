/* ============================================================
   ANIMATIONS.JS — Intersection Observer scroll reveal
   ============================================================ */

(function () {
  'use strict';

  var revealSelectors = '.reveal, .reveal-left, .reveal-right, .reveal-scale';
  var elements = document.querySelectorAll(revealSelectors);

  if (!('IntersectionObserver' in window)) {
    /* Fallback: reveal everything immediately */
    elements.forEach(function (el) {
      el.classList.add('revealed');
    });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          obs.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: '0px 0px -60px 0px'
    }
  );

  elements.forEach(function (el) {
    observer.observe(el);
  });
})();
