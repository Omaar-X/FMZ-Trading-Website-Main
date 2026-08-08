/* ============================================================
   CATALOG.JS — filter the catalogue library by product range
   ============================================================ */

(function () {
  'use strict';

  var filters = document.querySelectorAll('.cat-filter');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.cat-card'));
  var featured = document.querySelector('.cat-featured');
  var counter = document.getElementById('catCount');

  if (!filters.length || !cards.length) return;

  function label(count, filter) {
    if (filter === 'all') return 'Showing all ' + (count + 1) + ' catalogues';
    if (count === 0) return 'No catalogue in this range yet';
    return 'Showing ' + count + (count === 1 ? ' catalogue' : ' catalogues');
  }

  function apply(filter) {
    var shown = 0;

    cards.forEach(function (card) {
      var match = filter === 'all' || card.getAttribute('data-cat') === filter;
      card.classList.toggle('is-hidden', !match);
      if (match) {
        shown++;
        /* cards revealed after a filter change never met the observer */
        card.classList.add('revealed');
      }
    });

    if (featured) featured.classList.toggle('is-hidden', filter !== 'all');
    if (counter) counter.textContent = label(shown, filter);
  }

  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filters.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      apply(btn.getAttribute('data-filter'));
    });
  });
})();
