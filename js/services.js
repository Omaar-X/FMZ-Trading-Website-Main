/* ============================================================
   SERVICES.JS — service card hover interactions
   Adds a subtle tilt / spotlight follow on the large cards
   ============================================================ */

(function () {
  'use strict';

  var cards = document.querySelectorAll('.service-full-card');
  if (!cards.length) return;

  var supportsHover = window.matchMedia('(hover: hover)').matches;

  cards.forEach(function (card) {
    if (supportsHover) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        var cx = rect.width / 2;
        var cy = rect.height / 2;
        var rotateX = ((y - cy) / cy) * -3;
        var rotateY = ((x - cx) / cx) * 3;
        card.style.transform =
          'translateY(-8px) perspective(900px) rotateX(' +
          rotateX +
          'deg) rotateY(' +
          rotateY +
          'deg)';
      });

      card.addEventListener('mouseleave', function () {
        card.style.transform = '';
      });
    }
  });
})();
