from django.contrib import admin
from .models import Page, Category, UserProfile


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # auto fill in admin interface

admin.site.register(Page)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
