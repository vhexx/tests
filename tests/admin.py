from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from django.forms import ModelForm
from django.http import HttpResponseRedirect

class AnswerInline(admin.StackedInline):
	model = AnswerPrototype

class QuestionForm(ModelForm):
	class Meta:
		model = QuestionPrototype
	test_id = None
	def __init__(self, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		if test_id:
			self.fields['test'].initial = test_id

class QuestionAdmin(admin.ModelAdmin):
	model = QuestionPrototype
	inlines = [AnswerInline]
	form = QuestionForm
	def add_view(self, request, obj, form, change):
		if test_id in request:
			QuestionAdmin.form.test_id = int(request.test_id)
		return super(QuestionAdmin, self).add_view(self, request, obj, form, change)
    

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    def response_add(self, request, obj, post_url_continue=None):
    	return HttpResponseRedirect('../../questionprototype/add/?test_id='+str(obj.id))

admin.site.register(QuestionPrototype, QuestionAdmin)
admin.site.register(TestPrototype, TestAdmin)