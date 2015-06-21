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
            self.Meta.fields['test'].queryset = TestPrototype.objects.get(pk=self.test_id)
            #self.Meta.readonly_fields = ('test',)
        super(QuestionForm, self).__init__(*args, **kwargs)

class QuestionAdmin(admin.ModelAdmin):
    model = QuestionPrototype
    inlines = [AnswerInline]
    form = QuestionForm

    def add_view(self, request, form_url='', extra_context=None):
        test_id = request.GET.get('test_id')
        self.form.test_id = test_id
        print('test_id:'+str(test_id))
        return super(QuestionAdmin, self).add_view(request, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('../../questionprototype/add?test_id=%s' % str(self.form.test_id))

    def delete_model(request, obj):
        obj.delete()
        return super(QuestionAdmin, self).delete_model(request, obj)

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('../../questionprototype/add?test_id=%s' % str(obj.id))

    def delete_model(request, obj):
        obj.delete()
        return super(TestAdmin, self).delete_model(request, obj)


admin.site.register(QuestionPrototype, QuestionAdmin)
admin.site.register(TestPrototype, TestAdmin)
