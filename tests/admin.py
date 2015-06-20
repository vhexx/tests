from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from django.http import HttpResponseRedirect

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    def response_add(self, request, obj, post_url_continue=None):
    	#if form.is_valid():
    	return HttpResponseRedirect('../../questionprototype')
    	#else:
    		#return HttpResponseRedirect('../../')

admin.site.register(TestPrototype, TestAdmin)