/* ============================================================
   HOME.JS — counter animation for stats section, scroll progress
   ============================================================ */

(function () {
  'use strict';

  var progressBar = document.getElementById('scrollProgressBar');
  if (progressBar) {
    var updateProgress = function () {
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var pct = docHeight > 0 ? (window.scrollY / docHeight) * 100 : 0;
      progressBar.style.width = pct + '%';
    };
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }
})();

(function () {
  'use strict';

  var counters = document.querySelectorAll('.stat-number[data-target]');
  if (!counters.length) return;

  var animated = false;

  function animateCounter(el) {
    var target = parseFloat(el.getAttribute('data-target'));
    var suffix = el.getAttribute('data-suffix') || '';
    var duration = 2000;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      /* easeOutExpo for a nice deceleration */
      var eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      var value = Math.floor(eased * target);
      el.innerHTML = value + '<span class="suffix">' + suffix + '</span>';
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.innerHTML = target + '<span class="suffix">' + suffix + '</span>';
      }
    }

    requestAnimationFrame(step);
  }

  function runAll() {
    if (animated) return;
    animated = true;
    counters.forEach(animateCounter);
  }

  var statsSection = document.querySelector('.stats');

  if ('IntersectionObserver' in window && statsSection) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            runAll();
            observer.disconnect();
          }
        });
      },
      { threshold: 0.4 }
    );
    observer.observe(statsSection);
  } else {
    runAll();
  }
})();
