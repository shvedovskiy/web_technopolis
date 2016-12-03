from django.contrib import admin
from .models import Post, Comment


class PostInline(admin.StackedInline):
    model = Comment
    extra = 2


class PostAdmin(admin.ModelAdmin):
    fields = [
        'author',
        'title',
        'text',
        'created_date',
        'published_date',
    ]
    inlines = [PostInline]
    list_filter = ['created_date']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
