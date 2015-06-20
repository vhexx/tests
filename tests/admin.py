from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from django.http import HttpResponseRedirect

class AnswerInline(admin.StackedInline):
	model = AnswerPrototype

class QuestionAdmin(admin.ModelAdmin):
	model = QuestionPrototype
	inlines = [AnswerInline]
	#def add_view(self, request, obj, form, change):
		#return super(QuestionAdmin, self).add_view(self, request, obj, form, change)

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    def response_add(self, request, obj, post_url_continue=None):
    	return HttpResponseRedirect('../../questionprototype?test_id='+obj.id)

admin.site.register(QuestionPrototype, QuestionAdmin)
admin.site.register(TestPrototype, TestAdmin)