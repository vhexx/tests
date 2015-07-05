$(window).on('load', function () {
  $('#loader').remove();
  $('#main_form div').css({'opacity' : '1.0'});
});
$(document).on('ready', function () {
  $('.img_choice_area img').on('click', function () {
    $(this).css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
  });
});