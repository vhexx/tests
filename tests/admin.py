from django.contrib import admin

def action1 (modeladmin, request, queryset):
    queryset.update(first_name='ivan')
action1.short_description = "action 1"
