/* ============================================================
   GALLERY.JS — filter buttons, lightbox open/close/navigate
   ============================================================ */

(function () {
  'use strict';

  var filterButtons = document.querySelectorAll('.filter-btn');
  var items = Array.prototype.slice.call(document.querySelectorAll('.masonry-item'));
  var loadMoreBtn = document.getElementById('galleryLoadMore');
  var galleryCount = document.getElementById('galleryCount');
  var activeFilter = 'all';
  var pageSize = window.matchMedia('(max-width: 768px)').matches ? 18 : 30;
  var shownLimit = pageSize;

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

      activeFilter = btn.getAttribute('data-filter');
      shownLimit = pageSize;
      renderGallery();
      btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    });
  });

  function renderGallery() {
    var matches = items.filter(function (item) {
      return activeFilter === 'all' || item.getAttribute('data-category') === activeFilter;
    });

    items.forEach(function (item) {
      item.classList.add('hide');
      item.classList.remove('load-hidden');
    });

    matches.forEach(function (item, index) {
      if (index < shownLimit) item.classList.remove('hide');
      else item.classList.add('load-hidden');
    });

    var shown = Math.min(shownLimit, matches.length);
    if (galleryCount) galleryCount.textContent = 'Showing ' + shown + ' of ' + matches.length + ' projects';
    if (loadMoreBtn) loadMoreBtn.hidden = shown >= matches.length;
    rebuildVisible();
  }

  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function () {
      shownLimit += pageSize;
      renderGallery();
    });
  }

  function rebuildVisible() {
    visibleItems = items.filter(function (item) {
      return !item.classList.contains('hide') && !item.classList.contains('load-hidden');
    });
  }

  renderGallery();

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

/* ---------- SECTION TABS: Photos | Site Films ----------
   Sticky under the navbar; highlights whichever section fills the
   middle of the screen, and counts the photo tiles for its badge. */
(function () {
  'use strict';

  var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-work-tab]'));
  if (!tabs.length) return;

  var photoCount = document.querySelector('[data-photo-count]');
  if (photoCount) photoCount.textContent = document.querySelectorAll('.masonry-item').length;

  function setActive(key) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-work-tab') === key;
      t.classList.toggle('is-active', on);
      if (on) t.setAttribute('aria-current', 'true');
      else t.removeAttribute('aria-current');
    });
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () { setActive(t.getAttribute('data-work-tab')); });
  });

  /* the navbar shrinks once scrolled, so the bar docks to its live bottom
     edge rather than a guessed height; anchors land just below both */
  var bar = document.querySelector('.work-tabs');
  var navbar = document.getElementById('navbar');
  var queued = false;
  function dock() {
    queued = false;
    if (!bar || !navbar) return;
    var top = Math.max(0, Math.round(navbar.getBoundingClientRect().bottom));
    bar.style.top = top + 'px';
    document.documentElement.style.setProperty('--work-offset', (top + bar.offsetHeight + 16) + 'px');
  }
  function queueDock() {
    if (queued) return;
    queued = true;
    window.requestAnimationFrame(dock);
  }
  window.addEventListener('scroll', queueDock, { passive: true });
  window.addEventListener('resize', queueDock);
  if (navbar) navbar.addEventListener('transitionend', queueDock);
  dock();

  /* arriving on gallery.html#films: the browser jumps before the photos
     above have loaded, then they push the section away — re-land on it */
  var hashTarget = location.hash && document.getElementById(location.hash.slice(1));
  if (hashTarget && tabs.some(function (t) { return '#' + t.getAttribute('data-work-tab') === location.hash; })) {
    setActive(hashTarget.id);
    window.addEventListener('load', function () {
      dock();
      /* instant: a smooth glide from the top would pass the lazy photos,
         load them mid-flight and miss the target all over again */
      hashTarget.scrollIntoView({ behavior: 'instant', block: 'start' });
      /* the jump itself shrinks the navbar (0.4s), which moves the bars —
         settle once more when it has finished */
      window.setTimeout(function () {
        dock();
        hashTarget.scrollIntoView({ behavior: 'instant', block: 'start' });
      }, 480);
    });
  }

  if (!('IntersectionObserver' in window)) return;

  /* a band across the middle of the viewport: the section crossing it wins */
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) setActive(e.target.id);
    });
  }, { rootMargin: '-45% 0px -50% 0px' });

  tabs.forEach(function (t) {
    var target = document.getElementById(t.getAttribute('data-work-tab'));
    if (target) spy.observe(target);
  });
})();
