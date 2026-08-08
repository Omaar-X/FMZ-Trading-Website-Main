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
    btn.setAttribute('aria-pressed', btn.classList.contains('active') ? 'true' : 'false');

    btn.addEventListener('click', function () {
      filterButtons.forEach(function (b) {
        b.classList.remove('active');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed', 'true');

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

  /* whatever had focus before the dialog opened, so it can be handed back */
  var lastFocused = null;

  function openLightbox(item) {
    rebuildVisible();
    currentIndex = visibleItems.indexOf(item);
    updateLightbox();
    lastFocused = document.activeElement;
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    focusClose();
  }

  /* .open flips visibility with no transition delay (see .lightbox in
     gallery.css) so this normally lands straight away — but a hidden element
     silently refuses focus, so retry once on the next frame rather than
     leaving a keyboard user stranded outside the dialog they just opened. */
  function focusClose() {
    if (!closeBtn) return;
    closeBtn.focus();
    if (document.activeElement === closeBtn) return;
    window.requestAnimationFrame(function () {
      if (lightbox.classList.contains('open')) closeBtn.focus();
    });
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
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    /* send focus back to the tile that opened it, not to the top of the page */
    if (lastFocused && lastFocused.focus) lastFocused.focus();
    lastFocused = null;
  }

  function showNext() {
    currentIndex = (currentIndex + 1) % visibleItems.length;
    updateLightbox();
  }

  function showPrev() {
    currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
    updateLightbox();
  }

  /* the tiles are divs, so they need the button contract spelled out:
     reachable by Tab, announced as a button, and openable with Enter/Space */
  items.forEach(function (item) {
    var title = item.getAttribute('data-title') || '';
    var label = item.getAttribute('data-cat-label') || '';

    item.setAttribute('role', 'button');
    item.setAttribute('tabindex', '0');
    item.setAttribute('aria-label', 'View larger: ' + title + (label ? ' (' + label + ')' : ''));

    item.addEventListener('click', function () {
      openLightbox(item);
    });

    item.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();          /* Space would otherwise scroll the page */
        openLightbox(item);
      }
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if (nextBtn) nextBtn.addEventListener('click', showNext);
  if (prevBtn) prevBtn.addEventListener('click', showPrev);

  /* Click on backdrop closes */
  lightbox.addEventListener('click', function (e) {
    if (e.target === lightbox) closeLightbox();
  });

  /* Keyboard: ESC, arrows, and Tab kept inside the dialog */
  document.addEventListener('keydown', function (e) {
    if (!lightbox.classList.contains('open')) return;

    if (e.key === 'Escape') { closeLightbox(); return; }
    if (e.key === 'ArrowRight') { showNext(); return; }
    if (e.key === 'ArrowLeft') { showPrev(); return; }
    if (e.key !== 'Tab') return;

    var stops = [prevBtn, nextBtn, closeBtn].filter(Boolean);
    if (!stops.length) return;

    var at = stops.indexOf(document.activeElement);
    var next = e.shiftKey ? at - 1 : at + 1;
    if (at === -1 || next < 0 || next >= stops.length) {
      e.preventDefault();
      stops[e.shiftKey ? stops.length - 1 : 0].focus();
    }
  });
})();
