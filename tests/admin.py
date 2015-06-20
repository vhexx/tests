from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype

class QuestionInline(model.StackedInline):
    model = QuestionPrototype
    fk_name = 'test'
    extra = 3

class TestAdmin(model.ModelAdmin):
    model = TestPrototype
    inlines = [QuestionInline]
    extra = 3

admin.site.register(TestPrototype, TestAdmin)