/* ============================================================
   GALLERY.JS — filter buttons, lightbox open/close/navigate
   ============================================================ */

(function () {
  'use strict';

  var filterButtons = document.querySelectorAll('.filter-btn');
  var items = Array.prototype.slice.call(document.querySelectorAll('.masonry-item'));

  var lightbox = document.getElementById('lightbox');
  var lightboxImg = document.getElementById('lightboxImg');
  var lightboxCat = document.getElementById('lightboxCat');
  var lightboxTitle = document.getElementById('lightboxTitle');
  var lightboxCurrent = document.getElementById('lightboxCurrent');
  var lightboxTotal = document.getElementById('lightboxTotal');
  var closeBtn = document.getElementById('lightboxClose');
  var prevBtn = document.getElementById('lightboxPrev');
  var nextBtn = document.getElementById('lightboxNext');

  var currentIndex = 0;
  /* visibleItems = the items currently shown (respects active filter) */
  var visibleItems = items.slice();

  /* ---------- FILTERING ---------- */
  filterButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filterButtons.forEach(function (b) {
        b.classList.remove('active');
      });
      btn.classList.add('active');

      var filter = btn.getAttribute('data-filter');

      items.forEach(function (item) {
        var cat = item.getAttribute('data-category');
        if (filter === 'all' || cat === filter) {
          item.classList.remove('hide');
        } else {
          item.classList.add('hide');
        }
      });

      rebuildVisible();
    });
  });

  function rebuildVisible() {
    visibleItems = items.filter(function (item) {
      return !item.classList.contains('hide');
    });
  }

  /* ---------- LIGHTBOX ---------- */
  if (!lightbox) return;

  function openLightbox(item) {
    rebuildVisible();
    currentIndex = visibleItems.indexOf(item);
    updateLightbox();
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function updateLightbox() {
    var item = visibleItems[currentIndex];
    if (!item) return;
    var img = item.querySelector('img');
    var fullSrc = img.getAttribute('data-full') || img.getAttribute('src');
    lightboxImg.setAttribute('src', fullSrc);
    lightboxImg.setAttribute('alt', img.getAttribute('alt') || '');
    if (lightboxCat) lightboxCat.textContent = item.getAttribute('data-cat-label') || item.getAttribute('data-category');
    if (lightboxTitle) lightboxTitle.textContent = item.getAttribute('data-title') || '';
    if (lightboxCurrent) lightboxCurrent.textContent = currentIndex + 1;
    if (lightboxTotal) lightboxTotal.textContent = visibleItems.length;
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  function showNext() {
    currentIndex = (currentIndex + 1) % visibleItems.length;
    updateLightbox();
  }

  function showPrev() {
    currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
    updateLightbox();
  }

  items.forEach(function (item) {
    item.addEventListener('click', function () {
      openLightbox(item);
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if (nextBtn) nextBtn.addEventListener('click', showNext);
  if (prevBtn) prevBtn.addEventListener('click', showPrev);

  /* Click on backdrop closes */
  lightbox.addEventListener('click', function (e) {
    if (e.target === lightbox) closeLightbox();
  });

  /* Keyboard: ESC, arrows */
  document.addEventListener('keydown', function (e) {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    else if (e.key === 'ArrowRight') showNext();
    else if (e.key === 'ArrowLeft') showPrev();
  });
})();
