from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype

class QuestionInline(admin.StackedInline):
    model = QuestionPrototype
    fk_name = 'test'
    extra = 3

class TestAdmin(admin.ModelAdmin):
    model = TestPrototype
    inlines = [QuestionInline]
    extra = 3

admin.site.register(TestPrototype, TestAdmin)