from django.contrib import admin
from .models import TestPrototype, QuestionPrototype, AnswerPrototype, ImagePrototype

def action1 (modeladmin, request, queryset):
    queryset.update(first_name='ivan')
action1.short_description = "action 1"

admin.site.register(TestPrototype)
admin.site.register(QuestionPrototype)
admin.site.register(AnswerPrototype)
admin.site.register(ImagePrototype)