from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class AnswerInline(NestedStackedInline):
    model = AnswerPrototype
    extra = 2
    fk_name = 'question'

class QuestionInline(NestedStackedInline):
    model = QuestionPrototype
    extra = 1
    fk_name = 'test'
    inlines = [AnswerInline]

class TestAdmin(NestedModelAdmin):
    model = TestPrototype
    inlines = [QuestionInline]

admin.site.register(TestPrototype, TestAdmin)