from django.contrib import admin
from tests.models import Person

def action1 (modeladmin, request, queryset):
    queryset.update(first_name='ivan')
action1.short_description = "action 1"

class PersonAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    ordering = ['last_name']
    actions = [action1]

admin.site.register(Person, PersonAdmin)
