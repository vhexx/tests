from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
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
        if self.test_id:
            self.fields['test'].queryset = self.Meta.model.objects.get(pk=self.test_id)
            self.readonly_fields = ('test',)
        super(QuestionForm, self).__init__(*args, **kwargs)

class QuestionAdmin(admin.ModelAdmin):
    model = QuestionPrototype
    inlines = [AnswerInline]
    form = QuestionForm

    def add_view(self, request, form_url='', extra_context=None):
        test_id = request.GET.get('test_id')
        self.form.test_id = test_id
        #debug
        print('test_id:'+str(test_id))
        return super(QuestionAdmin, self).add_view(request, form_url, extra_context)


class TestAdmin(admin.ModelAdmin):
    model = TestPrototype

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('../../questionprototype/add?test_id=%s' % str(obj.id))


admin.site.register(QuestionPrototype, QuestionAdmin)
admin.site.register(TestPrototype, TestAdmin)
