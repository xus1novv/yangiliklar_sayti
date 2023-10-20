from django.contrib import admin
from .models import News, Category,Contact, Comment




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','publish_time', 'status']
    list_filter = ['status','created_tile', 'publish_time','category']
    #created_time ni .models.py da created_tile deb yozilgan!!!!!!!!!!!!!!!!!!!!
    prepopulated_fields = {'slug': ('title' ,)} # avtomatiski slugni titlening matni bilan to'ldiradi.
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_time']


admin.site.register(Contact)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'active_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)
    def active_comments(self, request, queryset):
        queryset.update(active=True)

