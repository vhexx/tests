from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from django.forms import ModelForm
from django.shortcuts import render

class QuestionForm(forms.ModelForm):
	class Meta:
		model = QuestionPrototype
	answers = forms.CharField(loabel='answers', max_length=100)

class QuestionAdmin(admin.ModelAdmin):
	model = QuestionPrototype
	#form = QuestionForm

class QuestionInline(admin.StackedInline):
    model = QuestionPrototype
    fk_name = 'test'
    extra = 3

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    inlines = [QuestionInline]

admin.site.register(QuestionPrototype, QuestionAdmin)
admin.site.register(TestPrototype, TestAdmin)