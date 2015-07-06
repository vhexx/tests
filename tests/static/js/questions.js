function checkboxes_valid(element)
{
	var checkboxes = element.find('input[type="checkbox"]');
	var checkbox_names_checked = {}, name='', checked_count = 0, len = checkboxes.length;
	for (var i=0; i<len; i++) {
		name = checkboxes.eq(i).attr('name');
		if (!(name in checkbox_names)) {
			checked_count = checkboxes.find('input[name='+cur_name+']:checked').length;
			if (checked_count > 0) {
				checkbox_names[cur_name] = checked_count;
			}
			else {
				alert('checkbox, name: '+name);
				return false;
			}
		}
	}
	return true;
}
function radios_valid(element)
{
	return true;
}
function selects_valid(element)
{
	return true;
}
$(document).ready(function() {
	var main_form = $('#main_form');
	$('#next').closest('form').on('submit', function(eventObject) {
		if (!( checkboxes_valid(main_form) && radios_valid(main_form) && selects_valid(main_form) )) {
			eventObject.preventDefault();
		}
	});
});