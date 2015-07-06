$(window).on('load', function () {
  $('#loader').remove();
  $('#main_form div').css({'opacity' : '1.0'});
});
$(document).on('ready', function () {
  $('.img_choice_area img').on('click', function () {
    $(this).css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
  });
  var img_blocks = $('.img_div');
  var left_form = $('#left_form');
  var right_form = $('#right_form');
  $(document).keydown(function (event) {
    switch(event.which)
    {
      case 37:
        img_blocks.eq(0).css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
        left_form.submit();
      case 39:
        img_blocks.eq(1).css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
        right_form.submit();
    }
  });
});