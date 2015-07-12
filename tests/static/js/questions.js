function checkboxes_valid(element)
{
	var res = true;
	var checkboxes = element.find('input[type="checkbox"]');
	var checkbox_names_checked = {}, name='', checked_count = 0, len = checkboxes.length;
	for (var i=0; i<len; i++) {
		name = checkboxes.eq(i).attr('name');
		if (!(name in checkbox_names_checked)) {
			checked_count = element.find('input[type="checkbox"][name="'+name+'"]:checked').length;
			if (checked_count > 0) {
				checkbox_names_checked[name] = checked_count;
				$('#'+name+'_question .required').css({'display' : 'none'});
			}
			else {
				$('#'+name+'_question .required').css({'display' : 'inline'});
				res = false;
			}
		}
	}
	return res;
}
function radios_valid(element)
{
	var res = true;
	var radios = element.find('input[type="radio"]');
	var len = radios.length, name='', radio_names_checked={};
	for (var i=0; i<len; i++) {
		name = radios.eq(i).attr('name');
		if (!(name in radio_names_checked)) {
		    if (element.find('input[type="radio"][name="'+name+'"]:checked').length == 0) {
			    $('#'+name+'_question .required').css({'display' : 'inline'});
			    res = false;
		    }
		    else {
			    radio_names_checked[name] = 1;
			    $('#'+name+'_question .required').css({'display' : 'none'});
		    }
		}
	}
	return res;
}

$(document).ready(function() {
	var main_form = $('#main_form');
	$('#next').closest('form').submit(function(eventObject) {
		if !( checkboxes_valid(main_form) {
			if !(radios_valid(main_form)) {
				alert('Пожалуйста, ответьте на все вопросы анкеты.');
			    eventObject.preventDefault();
			}
		}
	});
});