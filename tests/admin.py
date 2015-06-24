from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class AnswerInline(admin.StackedInline):
    model = AnswerPrototype

class QuestionForm(ModelForm):
    class Meta:
        model = QuestionPrototype

    test_id = None

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        if self.test_id:
            tests_set = TestPrototype.objects.filter(id=int(self.test_id))
            self.fields['test'] = forms.ModelChoiceField(queryset=tests_set, empty_label=None)

class QuestionAdmin(admin.ModelAdmin):
    model = QuestionPrototype
    inlines = [AnswerInline]
    form = QuestionForm

    def add_view(self, request, form_url='', extra_context=None):
        test_id = request.GET.get('test_id')
        self.form.test_id = test_id
        #print('test_id:'+str(test_id))
        return super(QuestionAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context=None):
        self.form.test_id = QuestionPrototype.objects.get(pk=object_id).test
        return super(QuestionAdmin, self).change_view(request, object_id, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('../../questionprototype/add?test_id=%s' % str(self.form.test_id))

class QuestionInline(admin.StackedInline):
    model = QuestionPrototype
    template = 'question_form.html'

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(TestAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [QuestionInline]
        return super(TestAdmin, self).change_view(request, object_id, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        #return HttpResponseRedirect('../../questionprototype/add?test_id=%s' % str(obj.id))
        return HttpResponseRedirect('../%s' % str(obj.id))

    def delete_model(self, request, obj):
        rel_questions = QuestionPrototype.objects.filter(test=obj.id)
        for q in rel_questions:
            AnswerPrototype.objects.filter(question=q.id).delete()
        rel_questions.delete()
        res = super(TestAdmin, self).delete_model(request, obj)
        if obj.id:
            obj.delete()
        return res


admin.site.register(QuestionPrototype, QuestionAdmin)
admin.site.register(TestPrototype, TestAdmin)
