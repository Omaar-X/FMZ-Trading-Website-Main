/* ============================================================
   VIDEO.JS — play background films only while they are on screen
   Keeps data and battery cost down, and respects reduced motion.
   ============================================================ */

(function () {
  'use strict';

  var videos = Array.prototype.slice.call(document.querySelectorAll('video.js-autoplay'));
  if (!videos.length) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduced) {
    /* poster only — never start playback */
    videos.forEach(function (v) {
      v.autoplay = false;
      v.removeAttribute('autoplay');
      v.pause();
    });
    return;
  }

  /* play() alone starts the fetch for preload="none" sources — calling load()
     first would abort it and leave the element paused on its poster. */
  function play(video) {
    var attempt = video.play();
    if (!attempt || !attempt.catch) return;

    attempt.catch(function () {
      /* not buffered yet, or the browser declined: try once more when ready */
      if (video.dataset.retried) return;
      video.dataset.retried = '1';
      video.addEventListener('canplay', function once () {
        video.removeEventListener('canplay', once);
        var second = video.play();
        if (second && second.catch) second.catch(function () {});
      });
    });
  }

  if (!('IntersectionObserver' in window)) {
    videos.forEach(play);
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.dataset.inview = '1';
        play(entry.target);
      } else {
        delete entry.target.dataset.inview;
        entry.target.pause();
      }
    });
  }, { threshold: 0.25 });

  videos.forEach(function (video) {
    observer.observe(video);
  });

  /* a backgrounded tab should not keep decoding frames — and coming back to
     the tab has to resume, since the observer will not fire again on its own */
  document.addEventListener('visibilitychange', function () {
    videos.forEach(function (v) {
      if (document.hidden) {
        v.pause();
      } else if (v.dataset.inview) {
        play(v);
      }
    });
  });
})();
