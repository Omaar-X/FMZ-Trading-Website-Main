/* ============================================================
   PREMIUM.JS — cursor glow, lightweight 3D tilt, hero parallax
   ============================================================ */

(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reducedMotion) return;

  var orb = document.createElement('div');
  orb.className = 'premium-orb';
  document.body.appendChild(orb);

  var pointerX = window.innerWidth * 0.5;
  var pointerY = window.innerHeight * 0.35;
  var targetX = pointerX;
  var targetY = pointerY;

  window.addEventListener('pointermove', function (event) {
    targetX = event.clientX;
    targetY = event.clientY;
  }, { passive: true });

  function moveOrb() {
    pointerX += (targetX - pointerX) * 0.12;
    pointerY += (targetY - pointerY) * 0.12;
    orb.style.left = pointerX + 'px';
    orb.style.top = pointerY + 'px';
    requestAnimationFrame(moveOrb);
  }
  moveOrb();

  var tiltItems = document.querySelectorAll(
    '.service-card, .service-full-card, .why-card, .value-card, .testimonial-card, .project-card, .founder-card, .contact-form-wrap'
  );

  tiltItems.forEach(function (item) {
    item.addEventListener('pointermove', function (event) {
      var rect = item.getBoundingClientRect();
      var x = (event.clientX - rect.left) / rect.width - 0.5;
      var y = (event.clientY - rect.top) / rect.height - 0.5;
      item.style.transform = 'perspective(900px) rotateX(' + (y * -3.5) + 'deg) rotateY(' + (x * 4.5) + 'deg) translateY(-6px)';
    });

    item.addEventListener('pointerleave', function () {
      item.style.transform = '';
    });
  });

  var headings = document.querySelectorAll('.section-title, .page-hero h1');
  headings.forEach(function (heading, index) {
    heading.classList.add('heading-dynamic');
    heading.style.setProperty('--heading-delay', (0.08 + (index % 4) * 0.08) + 's');
  });

  var hero = document.querySelector('.hero');
  var heroContent = document.querySelector('.hero-content');
  if (hero && heroContent) {
    window.addEventListener('scroll', function () {
      var scroll = Math.min(window.scrollY, hero.offsetHeight);
      heroContent.style.transform = 'translateY(' + (scroll * 0.08) + 'px)';
    }, { passive: true });
  }

  var offer = document.querySelector('.hero-offer');
  if (offer) {
    var offerData = [
      {
        theme: 'drapery',
        number: '01 / 03',
        visual: 'DRAPERY',
        tag: 'Signature interior edit',
        title: 'Soft layers.<br><em>Strong character.</em>',
        copy: 'Custom curtains and feature walls designed to make your space feel finished.',
        link: 'Explore the trend'
      },
      {
        theme: 'feature',
        number: '02 / 03',
        visual: 'FEATURE WALLS',
        tag: 'Trending finish',
        title: 'Make every wall.<br><em>worth noticing.</em>',
        copy: 'Textured wallpaper and TV feature walls with a signature UAE feel.',
        link: 'Explore feature walls'
      },
      {
        theme: 'flooring',
        number: '03 / 03',
        visual: 'FLOORING',
        tag: 'Modern foundation',
        title: 'Ground your space.<br><em>beautifully.</em>',
        copy: 'Premium parquet, vinyl and laminate with a clean, lasting finish.',
        link: 'Explore flooring'
      }
    ];
    var offerIndex = 0;
    var offerVisual = offer.querySelector('.offer-visual');
    var offerNumber = offer.querySelector('.offer-index');
    var offerWord = offer.querySelector('.offer-visual-word');
    var offerTag = offer.querySelector('.offer-tag');
    var offerTitle = offer.querySelector('.offer-copy h2');
    var offerCopy = offer.querySelector('.offer-copy p');
    var offerLink = offer.querySelector('.offer-link');

    function updateOffer() {
      var item = offerData[offerIndex];
      offer.classList.add('is-swapping');
      window.setTimeout(function () {
        offerVisual.className = 'offer-visual has-slideshow offer-theme-' + item.theme;
        offerNumber.textContent = item.number;
        offerWord.textContent = item.visual;
        offerTag.textContent = item.tag;
        offerTitle.innerHTML = item.title;
        offerCopy.textContent = item.copy;
        offerLink.firstChild.textContent = item.link;
        offer.classList.remove('is-swapping');
      }, 240);
    }

    window.setInterval(function () {
      offerIndex = (offerIndex + 1) % offerData.length;
      updateOffer();
    }, 4800);
  }

  var slideshow = document.getElementById('offerSlideshow');
  if (slideshow) {
    var slides = Array.prototype.slice.call(slideshow.querySelectorAll('img'));
    var slideIndex = 0;
    if (slides.length > 1) {
      window.setInterval(function () {
        slides[slideIndex].classList.remove('active');
        slideIndex = (slideIndex + 1) % slides.length;
        slides[slideIndex].classList.add('active');
      }, 1000);
    }
  }
})();
