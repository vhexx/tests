$(window).on('load', function () {
  $('#loader').remove();
  $('#main_form div').css({'opacity' : '1.0'});
});
$(document).on('ready', function () {
  $('.img_choice_area img').on('click', function () {
    $(this).css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
  });
  var left_form = $('#left_form');
  var right_form = $('#right_form');
  $(document).keydown(function (event) {
    switch(event.which)
    {
      case 37:
        left_form.closest('.img_div').css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
        left_form[0].submit();
      case 39:
        right_form.closest('.img_div').css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
        right_form[0].submit();
    }
  });
});