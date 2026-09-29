/* ============================================================
   PROJECT-FILMS.JS — silent on-site films from real FM Trading jobs
   One list drives the home reel ([data-film-reel]) and the gallery
   film wall ([data-film-grid]). Adding a clip = one line below plus
   its .mp4/.jpg pair in assets/Video/projects/.
   Load before video.js so the home reel joins its autoplay observer.
   ============================================================ */

(function () {
  'use strict';

  var BASE = 'assets/Video/projects/';

  /* shape: 'tall' (phone portrait), 'square', 'wide' (landscape)
     home:  shown in the home-page reel, in this order */
  var FILMS = [
    { slug: 'tv-wall-led-glass-partition',      cat: 'tv',       tag: 'TV Feature Wall', title: 'Backlit TV Wall & Glass Partition', shape: 'square', home: true },
    { slug: 'backlit-mirror-floating-tv-panel', cat: 'tv',       tag: 'TV Feature Wall', title: 'Backlit Mirror & Floating TV Panel', shape: 'tall', home: true },
    { slug: 'fluted-wood-corridor-led-lines',   cat: 'panels',   tag: 'Wall Panels',     title: 'Fluted Wood Corridor, LED Lines', shape: 'tall', home: true },
    { slug: 'complete-apartment-fit-out',       cat: 'fitout',   tag: 'Full Fit-Out',    title: 'Complete Apartment Fit-Out', shape: 'square', home: true },
    { slug: 'grey-blackout-curtains-sheers',    cat: 'curtain',  tag: 'Curtains',        title: 'Blackout Drapes Over Sheers', shape: 'wide', home: true },
    { slug: 'herringbone-oak-spc-floor',        cat: 'flooring', tag: 'Flooring',        title: 'Herringbone Oak SPC', shape: 'tall', home: true },
    { slug: 'tv-wall-lit-shelf-niche',          cat: 'tv',       tag: 'TV Feature Wall', title: 'TV Wall with Lit Shelf Niche', shape: 'tall' },
    { slug: 'grey-wallpaper-backlit-tv-wall',   cat: 'tv',       tag: 'TV Feature Wall', title: 'Textured Wallpaper TV Wall', shape: 'tall' },
    { slug: 'walnut-fluted-panels-led',         cat: 'panels',   tag: 'Wall Panels',     title: 'Walnut Fluted Panels', shape: 'tall' },
    { slug: 'beige-panels-floating-shelves',    cat: 'panels',   tag: 'Wall Panels',     title: 'Beige Panels & Floating Shelves', shape: 'tall' },
    { slug: 'walnut-panel-majlis-tv-unit',      cat: 'panels',   tag: 'Wall Panels',     title: 'Walnut-Panel Majlis', shape: 'tall' },
    { slug: 'full-height-wall-panelling',       cat: 'panels',   tag: 'Wall Panels',     title: 'Full-Height Wall Panelling', shape: 'tall' },
    { slug: 'panelled-hall-arched-entry',       cat: 'panels',   tag: 'Wall Panels',     title: 'Panelled Hall, Arched Entry', shape: 'tall' },
    { slug: 'grey-oak-spc-flooring',            cat: 'flooring', tag: 'Flooring',        title: 'Grey Oak SPC Flooring', shape: 'tall' }
  ];

  var FILTERS = [
    { key: 'all',      label: 'All Films' },
    { key: 'tv',       label: 'TV Walls' },
    { key: 'panels',   label: 'Wall Panels' },
    { key: 'flooring', label: 'Flooring' },
    { key: 'curtain',  label: 'Curtains' },
    { key: 'fitout',   label: 'Full Fit-Out' }
  ];

  var reel = document.querySelector('[data-film-reel]');
  var grid = document.querySelector('[data-film-grid]');
  if (!reel && !grid) return;

  /* every "N films" figure on the page follows the list above */
  Array.prototype.forEach.call(document.querySelectorAll('[data-film-total]'), function (el) {
    el.textContent = FILMS.length;
  });

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function pad(n) { return n < 10 ? '0' + n : String(n); }

  /* muted has to be set as a property as well as an attribute, or some
     browsers refuse the autoplay; the files carry no audio track anyway */
  function makeVideo(film, autoplay) {
    var v = document.createElement('video');
    v.muted = true;
    v.setAttribute('muted', '');
    v.loop = true;
    v.setAttribute('playsinline', '');
    v.setAttribute('preload', 'none');
    v.setAttribute('poster', BASE + film.slug + '.jpg');
    v.setAttribute('aria-hidden', 'true');
    v.setAttribute('disablepictureinpicture', '');
    if (autoplay) v.className = 'js-autoplay';
    var s = document.createElement('source');
    s.src = BASE + film.slug + '.mp4';
    s.type = 'video/mp4';
    v.appendChild(s);
    return v;
  }

  function makeCard(film, index, list, autoplay) {
    var card = document.createElement('button');
    card.type = 'button';
    card.className = 'film-card is-' + film.shape;
    card.setAttribute('data-cat', film.cat);
    card.setAttribute('aria-label', 'Play film: ' + film.title + ' (' + film.tag + ')');

    card.appendChild(makeVideo(film, autoplay));

    var idx = document.createElement('span');
    idx.className = 'film-index';
    idx.textContent = pad(index + 1);
    card.appendChild(idx);

    var play = document.createElement('span');
    play.className = 'film-play';
    play.setAttribute('aria-hidden', 'true');
    card.appendChild(play);

    var meta = document.createElement('span');
    meta.className = 'film-meta';
    meta.innerHTML = '<span class="film-tag"></span><span class="film-title"></span>';
    meta.firstChild.textContent = film.tag;
    meta.lastChild.textContent = film.title;
    card.appendChild(meta);

    card.addEventListener('click', function () {
      openPlayer(list(), list().indexOf(film), card);
    });
    return card;
  }

  /* ---------- HOME REEL: autoplays in view via video.js ---------- */
  if (reel) {
    var homeFilms = FILMS.filter(function (f) { return f.home; });
    var track = reel.querySelector('.reel-track');
    homeFilms.forEach(function (film, i) {
      track.appendChild(makeCard(film, i, function () { return homeFilms; }, true));
    });


    function step(dir) {
      var first = track.querySelector('.film-card');
      var gap = parseFloat(getComputedStyle(track).columnGap) || 18;
      var by = first ? first.getBoundingClientRect().width + gap : track.clientWidth * 0.8;
      track.scrollBy({ left: dir * by, behavior: reduced ? 'auto' : 'smooth' });
    }

    var prev = reel.querySelector('[data-reel-prev]');
    var next = reel.querySelector('[data-reel-next]');
    if (prev) prev.addEventListener('click', function () { step(-1); });
    if (next) next.addEventListener('click', function () { step(1); });

    function syncArrows() {
      var max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max;
    }
    track.addEventListener('scroll', syncArrows, { passive: true });
    window.addEventListener('resize', syncArrows);
    syncArrows();
  }

  /* ---------- GALLERY WALL: posters, preview on hover, filter chips ---------- */
  if (grid) {
    var active = 'all';
    var shown = FILMS.slice();
    var cards = FILMS.map(function (film, i) {
      var card = makeCard(film, i, function () { return shown; }, false);
      /* a wall of 14 films all playing at once is noise and data — preview
         only the one under the pointer; touch users tap into the player */
      if (canHover && !reduced) {
        var v = card.querySelector('video');
        card.addEventListener('mouseenter', function () {
          var p = v.play();
          if (p && p.catch) p.catch(function () {});
        });
        card.addEventListener('mouseleave', function () { v.pause(); });
      }
      grid.appendChild(card);
      return card;
    });

    /* closing tile: turns a viewer into an enquiry, and squares off the wall */
    var cta = document.createElement('a');
    cta.className = 'film-cta';
    cta.href = 'contact.html';
    cta.innerHTML =
      '<span class="film-tag">Your space next</span>' +
      '<span class="film-title">Want this finish at home?</span>' +
      '<span class="film-cta-copy">Free site visit and quote across Ajman, Dubai &amp; Sharjah.</span>' +
      '<span class="film-cta-go">Get a quote <span aria-hidden="true">↗</span></span>';
    grid.appendChild(cta);

    var bar = document.querySelector('[data-film-filters]');
    var count = document.querySelector('[data-film-count]');

    function applyFilter() {
      shown = FILMS.filter(function (f) { return active === 'all' || f.cat === active; });
      cards.forEach(function (card, i) {
        card.hidden = !(active === 'all' || FILMS[i].cat === active);
      });
      if (count) count.textContent = shown.length + (shown.length === 1 ? ' film' : ' films');
    }

    if (bar) {
      FILTERS.forEach(function (f) {
        var n = f.key === 'all' ? FILMS.length : FILMS.filter(function (x) { return x.cat === f.key; }).length;
        if (!n) return;
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'film-filter' + (f.key === active ? ' active' : '');
        b.setAttribute('aria-pressed', f.key === active ? 'true' : 'false');
        b.innerHTML = '<span></span><small></small>';
        b.firstChild.textContent = f.label;
        b.lastChild.textContent = n;
        b.addEventListener('click', function () {
          active = f.key;
          bar.querySelectorAll('.film-filter').forEach(function (x) {
            x.classList.toggle('active', x === b);
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          applyFilter();
        });
        bar.appendChild(b);
      });
    }
    applyFilter();
  }

  /* ---------- PLAYER (shared) ---------- */
  var modal, mVideo, mTag, mTitle, mCount, mClose, mPrev, mNext;
  var queue = [], at = 0, opener = null, pausedBehind = [];

  function buildPlayer() {
    modal = document.createElement('div');
    modal.className = 'film-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-hidden', 'true');
    modal.setAttribute('aria-labelledby', 'filmModalTitle');
    modal.innerHTML =
      '<button type="button" class="film-modal-close" aria-label="Close film">&times;</button>' +
      '<button type="button" class="film-modal-nav film-modal-prev" aria-label="Previous film">&#8249;</button>' +
      '<button type="button" class="film-modal-nav film-modal-next" aria-label="Next film">&#8250;</button>' +
      '<figure class="film-modal-stage">' +
        '<video muted loop playsinline controls disablepictureinpicture controlslist="nodownload noremoteplayback noplaybackrate"></video>' +
        '<figcaption><span class="film-modal-tag"></span><h3 id="filmModalTitle"></h3>' +
        '<span class="film-modal-count"></span></figcaption>' +
      '</figure>';
    document.body.appendChild(modal);

    mVideo = modal.querySelector('video');
    mVideo.muted = true;
    mTag = modal.querySelector('.film-modal-tag');
    mTitle = modal.querySelector('h3');
    mCount = modal.querySelector('.film-modal-count');
    mClose = modal.querySelector('.film-modal-close');
    mPrev = modal.querySelector('.film-modal-prev');
    mNext = modal.querySelector('.film-modal-next');

    /* nobody should be able to switch sound back on */
    mVideo.addEventListener('volumechange', function () {
      if (!mVideo.muted) mVideo.muted = true;
    });

    mClose.addEventListener('click', closePlayer);
    mPrev.addEventListener('click', function () { show(at - 1); });
    mNext.addEventListener('click', function () { show(at + 1); });
    modal.addEventListener('click', function (e) { if (e.target === modal) closePlayer(); });

    document.addEventListener('keydown', function (e) {
      if (!modal.classList.contains('open')) return;
      if (e.key === 'Escape') { closePlayer(); return; }
      if (e.key === 'ArrowRight') { show(at + 1); return; }
      if (e.key === 'ArrowLeft') { show(at - 1); return; }
      if (e.key !== 'Tab') return;
      var stops = [mClose, mPrev, mNext, mVideo].filter(function (el) { return !el.hidden; });
      var i = stops.indexOf(document.activeElement);
      var n = e.shiftKey ? i - 1 : i + 1;
      if (i === -1 || n < 0 || n >= stops.length) {
        e.preventDefault();
        stops[e.shiftKey ? stops.length - 1 : 0].focus();
      }
    });
  }

  function show(i) {
    at = (i + queue.length) % queue.length;
    var film = queue[at];
    mVideo.setAttribute('poster', BASE + film.slug + '.jpg');
    mVideo.src = BASE + film.slug + '.mp4';
    mVideo.className = 'is-' + film.shape;
    mTag.textContent = film.tag;
    mTitle.textContent = film.title;
    mCount.textContent = pad(at + 1) + ' / ' + pad(queue.length);
    mPrev.hidden = mNext.hidden = queue.length < 2;
    if (!reduced) {
      var p = mVideo.play();
      if (p && p.catch) p.catch(function () {});
    }
  }

  function openPlayer(list, index, from) {
    if (!modal) buildPlayer();
    queue = list;
    opener = from;
    /* the films behind the dialog stop decoding while it is open */
    pausedBehind = Array.prototype.filter.call(document.querySelectorAll('.film-card video'), function (v) {
      return !v.paused;
    });
    pausedBehind.forEach(function (v) { v.pause(); });

    show(index);
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    mClose.focus();
  }

  function closePlayer() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    mVideo.pause();
    mVideo.removeAttribute('src');
    mVideo.load();
    pausedBehind.forEach(function (v) {
      if (v.classList.contains('js-autoplay') && v.dataset.inview) {
        var p = v.play();
        if (p && p.catch) p.catch(function () {});
      }
    });
    pausedBehind = [];
    if (opener && opener.focus) opener.focus();
    opener = null;
  }
})();
