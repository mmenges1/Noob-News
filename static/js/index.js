$(document.getElementById("button1")).click(function() {
  $(document.getElementById("button1")).toggleClass("active");
  $(".title").toggleClass("active");
  $("nav").toggleClass("active");
});

var swiper = new Swiper('.blog-slider', {
      spaceBetween: 30,
      effect: 'fade',
      loop: true,
      mousewheel: {
        invert: false,
      },
      // autoHeight: true,
      pagination: {
        el: '.blog-slider__pagination',
        clickable: true,
      }
    });

function hideNavbar() {
  $("#noob-navigator").removeClass("d-none");
}

hideNavbar();
