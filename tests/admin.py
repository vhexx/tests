from django.contrib import admin
from .models import Test, Question, Answer, PreQuestion, PostQuestion
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class AnswerInline(admin.StackedInline):
    model = Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question

    last = None

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        if QuestionForm.last:
            QuestionForm.last += 1
            self.fields['order'].initial = QuestionForm.last


class PreQuestionAdmin(admin.ModelAdmin):
    model = PreQuestion
    inlines = [AnswerInline]
    readonly_fields = ('test',)


class PreQuestionInline(admin.StackedInline):
    model = PreQuestion
    template = 'question_form.html'
    form = QuestionForm


class PostQuestionAdmin(admin.ModelAdmin):
    model = PostQuestion
    inlines = [AnswerInline]
    readonly_fields = ('test',)


class PostQuestionInline(admin.StackedInline):
    model = PostQuestion
    template = 'question_form.html'
    form = QuestionForm


class TestAdmin(admin.ModelAdmin):
    model = Test

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(TestAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [PreQuestionInline, PostQuestionInline]
        QuestionForm.last = Question.objects.order_by('-order')[:1].get().order
        return super(TestAdmin, self).change_view(request, object_id, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('../%s' % str(obj.id))

    def delete_model(self, request, obj):
        # rel_prequestions = PreQuestionInline.objects.filter(test=obj.id)
        # for q in rel_prequestions:
        #     Answer.objects.filter(question=q.id).delete()
        # rel_prequestions.delete()
        #
        # res = super(TestAdmin, self).delete_model(request, obj)
        # if obj.id:
        #     obj.delete()
        # return res
        pass


admin.site.register(PreQuestion, PreQuestionAdmin)
admin.site.register(PostQuestion, PostQuestionAdmin)
admin.site.register(Test, TestAdmin)
