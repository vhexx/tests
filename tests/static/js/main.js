$(window).load(function () {
  $('#loader').remove();
  $('#main_form div').css({'opacity' : '1.0'});
  var left_button = $('#left');
  var right_button = $('#right');
  var button_pressed = false;
  function btnClick(btn)
  {
    btn.closest('.img_div').find('img').css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
    setTimeout(function() {btn[0].click();}, 100);
  }
  $(document).keydown(function (event) {
    if (! button_pressed) {
      switch(event.which)
      {
      case 37:
        btnClick(left_button);
        button_pressed = true;
        break;
      case 39:
        btnClick(right_button);
        button_pressed = true;
      }
    }
  });
  $('.img_div img').on('click', function() {
    if ($(this).closest('.img_div').find('#left').length > 0) {
      btnClick(left_button);
    }
    else {
      btnClick(right_button);
    }
  });
});