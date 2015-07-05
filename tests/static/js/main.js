$(window).on('load', function () {
  $('#loader').remove();
  $('#main_form div').css({'opacity' : '1.0'});
});
$(document).on('ready', function () {
  var pair = {
    input_left : $('.img_choice_area input.left'),
    img_left : $('.img_choice_area img.left'),
    input_right : $('.img_choice_area input.right'),
    img_right : $('.img_choice_area img.right')
  };
  function switch_img (a, b)
  {
    pair['input_'+a].attr({'checked' : 'checked'});
    pair['img_'+a].css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
    pair['input_'+b].removeAttr('checked');
    pair['img_'+b].css({'box-shadow' : 'none'});
  }
  $('.img_choice_area img').on('click', function () {
    if ($(this).hasClass('left')) {
      switch_img('left', 'right');
    }
    else {
      switch_img('right', 'left');
    }
  });
});