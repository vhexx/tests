from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from django.forms import ModelForm
from django.shortcuts import render

class QuestionAdmin(admin.ModelAdmin):
	model = QuestionPrototype
	add_form_template = 'question_form.html'
    #def add_view(self, request, form_url="", extra_context=None):
    	#return render(request, 'question_form.html', {'form' : self.form, 'i' : 5})

class QuestionInline(admin.StackedInline):
    model = QuestionPrototype
    fk_name = 'test'
    extra = 3

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    inlines = [QuestionInline]

admin.site.register(QuestionPrototype, QuestionAdmin)
admin.site.register(TestPrototype, TestAdmin)