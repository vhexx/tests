from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class AnswerInline(admin.StackedInline):
    model = AnswerPrototype

class QuestionAdmin(admin.ModelAdmin):
    model = QuestionPrototype
    inlines = [AnswerInline]
    readonly_fields = ('test',)

    #def response_change(request, obj):
        #return HttpResponseRedirect('../../testprototype/%s' % str(obj.test.id))

class QuestionInline(admin.StackedInline):
    model = QuestionPrototype
    template = 'question_form.html'

class AnswerInline1(admin.StackedInline):
    model = AnswerPrototype
    fields = ('question', 'statement', 'test')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "test":
            kwargs["queryset"] = TestPrototype.objects.all()
        return super(MyModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(TestAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [QuestionInline, AnswerInline1]
        return super(TestAdmin, self).change_view(request, object_id, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
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
