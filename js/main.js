/* ============================================================
   MAIN.JS — shared: smooth scroll, scroll-to-top, current year
   ============================================================ */

(function () {
  'use strict';

  /* ---------- Preloader: brief cosmetic reveal, never blocks content ---------- */
  var preloader = document.getElementById('preloader');
  if (preloader) {
    var minTimeReached = false;
    var pageLoaded = false;

    function tryHidePreloader() {
      if (minTimeReached && pageLoaded) {
        preloader.classList.add('is-hidden');
      }
    }

    window.setTimeout(function () {
      minTimeReached = true;
      tryHidePreloader();
    }, 450);

    if (document.readyState === 'complete') {
      pageLoaded = true;
    } else {
      window.addEventListener('load', function () {
        pageLoaded = true;
        tryHidePreloader();
      });
    }

    /* Safety net: never let it hang past 1.6s even on a slow connection */
    window.setTimeout(function () {
      preloader.classList.add('is-hidden');
    }, 1600);

    tryHidePreloader();
  }

  /* ---------- Smooth scroll for in-page anchors ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#' || targetId.length < 2) return;
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ---------- Scroll to top button ---------- */
  var scrollTopBtn = document.getElementById('scrollTop');
  if (scrollTopBtn) {
    window.addEventListener('scroll', function () {
      if (window.pageYOffset > 500) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    });

    scrollTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- Auto current year in footer ---------- */
  var yearEls = document.querySelectorAll('.current-year');
  var year = new Date().getFullYear();
  yearEls.forEach(function (el) {
    el.textContent = year;
  });
})();
