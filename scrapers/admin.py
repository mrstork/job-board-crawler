from django.contrib import admin
from .models import Company, Position

def ignore(modeladmin, request, queryset):
    for company in queryset:
        company.ignore()
ignore.short_description = "Ignore selected companies"

class CompanyAdmin(admin.ModelAdmin):
    ordering = ['name']
    actions = [ignore]
    list_filter = (
        ('ignored', admin.BooleanFieldListFilter),
    )

class PositionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company, CompanyAdmin)
admin.site.register(Position, PositionAdmin)
