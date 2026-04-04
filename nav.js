(function () {
  function setupHeader(header) {
    var nav = header.querySelector('.site-nav');
    var toggle = header.querySelector('.nav-toggle');
    if (!nav || !toggle) {
      return;
    }

    function updateLayout() {
      var narrow = window.matchMedia('(max-width: 900px)').matches;
      var overflowing = header.scrollWidth > header.clientWidth + 1;
      var collapsible = narrow || overflowing;

      if (collapsible) {
        header.classList.add('is-collapsible');
      } else {
        header.classList.remove('is-collapsible');
        header.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    }

    toggle.addEventListener('click', function () {
      if (!header.classList.contains('is-collapsible')) {
        return;
      }
      var open = header.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    window.addEventListener('resize', updateLayout);
    updateLayout();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var headers = document.querySelectorAll('.site-header');
    for (var i = 0; i < headers.length; i += 1) {
      setupHeader(headers[i]);
    }
  });
})();
