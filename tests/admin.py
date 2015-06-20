from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class AnswerInline(NestedTabularInline):
    model = AnswerPrototype
    fk_name = 'question'

class QuestionInline(NestedStackedInline):
    model = QuestionPrototype
    fk_name = 'test'
    inlines = [AnswerInline]
    extra = 3

class TestAdmin(NestedModelAdmin):
    model = TestPrototype
    inlines = [QuestionInline]
    extra = 3

admin.site.register(AnswerPrototype)
admin.site.register(QuestionPrototype)
admin.site.register(TestPrototype, TestAdmin)