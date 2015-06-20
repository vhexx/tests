from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class AnswerInline(admin.StackedInline):
    model = AnswerPrototype
    extra = 2
    fk_name = 'question'

class QuestionInline(admin.StackedInline):
    model = QuestionPrototype
    extra = 1
    fk_name = 'test'
    inlines = [AnswerInline]

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    inlines = [QuestionInline]

admin.site.register(TestPrototype, TestAdmin)