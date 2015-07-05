$(window).on('load', function () {
  $('#loader').remove();
  $('#main_form').css({'display' : 'block'})
});
$(document).on('ready', function () {
  var left = $('.img_choice_area').find('input.left');
  var right = $('.img_choice_area').find('input.right');
  $('.img_choice_area img').on('click', function () {
    if ($(this).hasClass('left')) {
      left.attr({'checked' : 'checked'});
      right.removeAttr('checked');
    }
    else {
      left.removeAttr('checked');
      right.attr({'checked' : 'checked'});
    }
  });
});