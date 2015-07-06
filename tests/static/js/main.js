$(document).ready(function () {
	var main_area = $('#main_area');
	if (main_area.css('display') == 'none') {
		main_area[0].innerHTML = 'Разрешение экрана Вашего устройства недостаточно для прохождения теста. Пожалуйста, воспользуйтесь устройством с более высоким разрешением. Спасибо.';
	}
});