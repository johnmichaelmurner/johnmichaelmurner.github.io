document.addEventListener("DOMContentLoaded", function () {
  var headers = document.querySelectorAll(".site-header");

  for (var i = 0; i < headers.length; i += 1) {
    setupHeader(headers[i]);
  }

  function setupHeader(header) {
    var toggle = header.querySelector(".nav-toggle");
    if (!toggle) {
      return;
    }

    toggle.addEventListener("click", function (event) {
      event.stopPropagation();
      var isOpen = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    document.addEventListener("click", function (event) {
      if (!header.contains(event.target)) {
        header.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 900) {
        header.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }
});
