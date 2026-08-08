/* ============================================================
   NAVBAR.JS — transparent to solid on scroll, hamburger toggle
   ============================================================ */

(function () {
  'use strict';

  var navbar = document.getElementById('navbar');
  var hamburger = document.getElementById('hamburger');
  var mobileMenu = document.getElementById('mobileMenu');

  /* ---------- Transparent -> solid on scroll ---------- */
  function handleScroll() {
    if (!navbar) return;
    if (window.pageYOffset > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', handleScroll);
  handleScroll();

  /* ---------- Hamburger toggle ---------- */
  function closeMenu() {
    if (hamburger) {
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
    if (mobileMenu) mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (hamburger && mobileMenu) {
    /* the button owns the menu — say so, and keep the state in sync */
    if (mobileMenu.id) hamburger.setAttribute('aria-controls', mobileMenu.id);
    hamburger.setAttribute('aria-expanded', 'false');

    hamburger.addEventListener('click', function () {
      var isOpen = mobileMenu.classList.toggle('open');
      hamburger.classList.toggle('open', isOpen);
      hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    /* Close when a mobile link is clicked */
    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });

    /* Close on ESC — focus goes back to the button, not nowhere */
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !mobileMenu.classList.contains('open')) return;
      closeMenu();
      hamburger.focus();
    });
  }
})();
