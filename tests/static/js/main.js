$(window).on('load', function () {
  $('#loader').remove();
  $('#main_form div').css({'opacity' : '1.0'});
});
$(document).on('ready', function () {
  $('.img_choice_area img').on('click', function () {
    $(this).css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
  });
  var left_button = $('#left_button');
  var right_button = $('#right_button');
  $(document).keydown(function (event) {
    switch(event.which)
    {
      case 37:
        left_button.closest('.img_div').css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
        left_button[0].click();
      case 39:
        right_button.closest('.img_div').css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
        right_button[0].click();
    }
  });
});