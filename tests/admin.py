from django.contrib import admin
from .models import Test, Question, Answer, PreQuestion, PostQuestion, Image, ImagePair, FailureCriterion, FCFunction, QuestionType
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
import os
from django.contrib.admin import widgets
from django.utils.safestring import mark_safe


class ImageInlineFormset(forms.models.BaseInlineFormSet):
    def save(self, commit=True):
        for f in self.deleted_forms:
            os.remove(f.instance.img.path)
        return super(ImageInlineFormset, self).save(commit)


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0
    template = 'inline_image_form.html'
    formset = ImageInlineFormset
    fields = (('name', 'img', ), )


class ImagePairInline(admin.StackedInline):
    model = ImagePair
    fk_name = 'test'
    extra = 0
    fields = (('left', 'right', 'repeats', ), )

    test_id = None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.test_id and ((db_field.name == 'left') or (db_field.name == 'right')):
            kwargs['queryset'] = Image.objects.filter(test=self.test_id)
        return super(ImagePairInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class AnswerInline(admin.StackedInline):
    model = Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = QuestionType.objects.latest('id')
        self.fields['title'].initial = 'question'


class PreQuestionAdmin(admin.ModelAdmin):
    model = PreQuestion
    inlines = [AnswerInline]
    readonly_fields = ('test',)

    def delete_model(self, request, obj):
        rel_answers = Answer.objects.filter(question=obj.question_ptr)
        rel_answers.delete()
        par = Question.objects.get(id=obj.question_ptr)
        obj.delete()
        par.delete()

    def get_model_perms(self, request):
        return {}

    def response_change(self, request, obj):
        return HttpResponseRedirect('../../test/%s' % str(obj.test.id))


class PreQuestionInline(admin.StackedInline):
    model = PreQuestion
    template = 'question_form.html'
    form = QuestionForm
    extra = 0
    fields = (('isSeparator', 'order', ), ('title', 'type', ), )


class PostQuestionAdmin(admin.ModelAdmin):
    model = PostQuestion
    inlines = [AnswerInline]
    readonly_fields = ('test',)

    def delete_model(self, request, obj):
        PreQuestionAdmin.delete_model(self, request, obj)

    def get_model_perms(self, request):
        return {}

    def response_change(self, request, obj):
        return PreQuestionAdmin.response_change(self, request, obj)


class PostQuestionInline(admin.StackedInline):
    model = PostQuestion
    template = 'question_form.html'
    form = QuestionForm
    extra = 0
    fields = PreQuestionInline.fields


class FailureCriterionForm(forms.ModelForm):
    class Meta:
        model = FailureCriterion

    test_id = None

    def __init__(self, *args, **kwargs):
        super(FailureCriterionForm, self).__init__(*args, **kwargs)
        if (self.test_id):
            prequestions = PreQuestion.objects.filter(test=self.test_id)
            self.fields['question'].queryset = prequestions
            prequest_id_list = [x.id for x in prequestions]
            self.fields['answer'].queryset = Answer.objects.filter(question__in=prequest_id_list)


class FailureCriterionInline(admin.StackedInline):
    model = FailureCriterion
    fk_name = 'test'
    form = FailureCriterionForm
    extra = 0
    template = 'inline_failurecriterion_form.html'


class FCFunctionInline(admin.StackedInline):
    model = FCFunction
    fk_name = 'test'
    max_num = 1

    def has_add_permition(self, request):
        super(FCFunctionInline, self).has_add_permition(request)
        return False


class MultiFileInput(widgets.AdminFileWidget):
    def render(self, name, value, attrs=None):
        attrs['multiple'] = 'true'
        output = super(MultiFileInput, self).render(name, value, attrs=attrs)
        return mark_safe(output)


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'seconds', 'description', 'images']

    images = forms.ImageField(required=False, widget=MultiFileInput)


class TestAdmin(admin.ModelAdmin):
    model = Test

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(TestAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.form = TestForm
        self.inlines = [ImageInline, ImagePairInline, 
                        PreQuestionInline, PostQuestionInline,
                        FailureCriterionInline, FCFunctionInline]
        questions = Question.objects.filter(test=object_id)
        if questions:
            QuestionForm.last = questions.order_by('-order')[:1].get().order
        ImagePairInline.test_id = object_id
        FailureCriterionForm.test_id = object_id
        #for ajax filtration
        if (request.method == 'GET') and ('fc_filter' in request.GET):
            quest_id = int(request.GET.get('fc_filter', None))
            if quest_id:
                id_str = ''
                for i in Answer.objects.filter(question=quest_id):
                    id_str += str(i.id) + ' '
                return HttpResponse(id_str)
        default_return = super(TestAdmin, self).change_view(request, object_id, form_url, extra_context)
        #for adding multiple images
        loaded_images = request.FILES.getlist('images', [])
        for i in loaded_images:
            new_image = Image(name=i.name, img=i, test=Test.objects.get(id=object_id))
            new_image.save()
        return default_return

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('../%s' % str(obj.id))


admin.site.register(PreQuestion, PreQuestionAdmin)
admin.site.register(PostQuestion, PostQuestionAdmin)
admin.site.register(Test, TestAdmin)
