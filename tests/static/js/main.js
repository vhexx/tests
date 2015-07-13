$(document).ready(function () {
	var main_area = $('#main_area');
	var small_screen_message = 'Разрешение экрана Вашего устройства недостаточно для прохождения теста. Пожалуйста, воспользуйтесь устройством с более высоким разрешением. Спасибо.';
	if (main_area.css('display') == 'none') {
		main_area[0].remove();
		$('#footer')[0].innerHTML = small_screen_message;
	}
});