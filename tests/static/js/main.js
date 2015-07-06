$(window).on('load', function () {
  $('#loader').remove();
  $('#main_form div').css({'opacity' : '1.0'});
});
$(document).on('ready', function () {
  $('.img_choice_area img').on('click', function () {
    $(this).css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
  });
  var left_button = $('#left');
  var right_button = $('#right');
  function btnClick(btn)
  {
    btn.closest('.img_div').find('img').css({'box-shadow' : '0px 0px 6px 3px rgb(54, 141, 218)'});
    setInterval(function() {btn[0].click();}, 100);
  }
  $(document).keydown(function (event) {
    switch(event.which)
    {
      case 37:
        btnClick(left_button);
      case 39:
        btnClick(right_button);
    }
  });
  /*$('.img_div img').on('click', function() {
    if ($(this).closest('.img_div').find('#left').length > 0) {
      btnClick(left_button);
    }
    else {
      btnClick(right_button);
    }
  });*/
});