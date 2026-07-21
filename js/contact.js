/* ============================================================
   CONTACT.JS — form validation + WhatsApp redirect
   ============================================================ */

(function () {
  'use strict';

  var form = document.getElementById('contactForm');
  if (!form) return;

  var successBox = document.getElementById('formSuccess');
  /* Primary WhatsApp number used for the redirect */
  var WA_NUMBER = '971567275998';

  function setError(group, hasError) {
    if (hasError) group.classList.add('error');
    else group.classList.remove('error');
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function isValidPhone(phone) {
    return /^[+]?[\d\s()-]{7,}$/.test(phone);
  }

  function validate() {
    var valid = true;

    var name = form.querySelector('#name');
    var phone = form.querySelector('#phone');
    var email = form.querySelector('#email');
    var message = form.querySelector('#message');

    if (!name.value.trim()) {
      setError(name.closest('.form-group'), true);
      valid = false;
    } else setError(name.closest('.form-group'), false);

    if (!isValidPhone(phone.value.trim())) {
      setError(phone.closest('.form-group'), true);
      valid = false;
    } else setError(phone.closest('.form-group'), false);

    if (!isValidEmail(email.value.trim())) {
      setError(email.closest('.form-group'), true);
      valid = false;
    } else setError(email.closest('.form-group'), false);

    if (!message.value.trim()) {
      setError(message.closest('.form-group'), true);
      valid = false;
    } else setError(message.closest('.form-group'), false);

    return valid;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!validate()) return;

    var name = form.querySelector('#name').value.trim();
    var phone = form.querySelector('#phone').value.trim();
    var email = form.querySelector('#email').value.trim();
    var service = form.querySelector('#service').value;
    var message = form.querySelector('#message').value.trim();

    /* Build a pre-filled WhatsApp message */
    var text =
      'Hello FM Trading F.Z.E,%0A%0A' +
      'Name: ' + encodeURIComponent(name) + '%0A' +
      'Phone: ' + encodeURIComponent(phone) + '%0A' +
      'Email: ' + encodeURIComponent(email) + '%0A' +
      'Service: ' + encodeURIComponent(service || 'General Inquiry') + '%0A' +
      'Message: ' + encodeURIComponent(message);

    var waUrl = 'https://wa.me/' + WA_NUMBER + '?text=' + text;

    if (successBox) successBox.classList.add('show');

    /* Give the user a moment to see the confirmation, then redirect */
    setTimeout(function () {
      window.open(waUrl, '_blank');
    }, 800);

    form.reset();

    setTimeout(function () {
      if (successBox) successBox.classList.remove('show');
    }, 6000);
  });

  /* Clear error state while typing */
  form.querySelectorAll('input, select, textarea').forEach(function (field) {
    field.addEventListener('input', function () {
      var group = field.closest('.form-group');
      if (group) group.classList.remove('error');
    });
  });
})();
