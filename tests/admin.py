from django.contrib import admin
from .models import Test, Question, Answer, PreQuestion
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class AnswerInline(admin.StackedInline):
    model = Answer


class PreQuestionAdmin(admin.ModelAdmin):
    model = PreQuestion
    inlines = [AnswerInline]
    readonly_fields = ('test',)

    # def response_change(request, obj):
    #return HttpResponseRedirect('../../testprototype/%s' % str(obj.test.id))


class PreQuestionInline(admin.StackedInline):
    model = PreQuestion
    template = 'question_form.html'


class TestAdmin(admin.ModelAdmin):
    model = Test

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(TestAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [PreQuestionInline, ]
        return super(TestAdmin, self).change_view(request, object_id, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('../%s' % str(obj.id))

    def delete_model(self, request, obj):
        rel_questions = PreQuestionInline.objects.filter(test=obj.id)
        for q in rel_questions:
            Answer.objects.filter(question=q.id).delete()
        rel_questions.delete()
        res = super(TestAdmin, self).delete_model(request, obj)
        if obj.id:
            obj.delete()
        return res


admin.site.register(PreQuestion, PreQuestionAdmin)
admin.site.register(Test, TestAdmin)
