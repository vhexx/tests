from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

class addQuestionsForm(forms.Form):
	message = forms.CharField(max_length=100)

def add_questions(modeladmin, request, queryset):
	form = None
	if request.method == 'POST':
		form = addQuestionsForm(request.POST)
		if form.is_valid():
			message = form.cleaned_data['message']
			modeladmin.message_user(request, "%s !!!" % (message))
			return HttpResponseRedirect('base_site.html')
	if not form:
		form = addQuestionsForm()
	return render(request, '/workspace/tests/tests/static/admin/addquestions.html', {'form' : form})

class QuestionInline(admin.StackedInline):
	model = QuestionPrototype

class TestAdmin(admin.ModelAdmin):
	actions = [add_questions]
	inlines = [QuestionInline]

admin.site.register(TestPrototype, TestAdmin)