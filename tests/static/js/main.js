$(document).ready(function () {
	var main_area = $('#main_area');
	var small_screen_message = '���������� ������ ������ ���������� ������������ ��� ����������� �����. ����������, �������������� ����������� � ����� ������� �����������. �������.';
	if (main_area.css('display') == 'none') {
		main_area[0].remove();
		$('#footer')[0].innerHTML = small_screen_message;
	}
});