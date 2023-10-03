from django.contrib import admin
from .models import News, Category,Contact




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','publish_time', 'status']
    list_filter = ['status','created_tile', 'publish_time','category']
    #created_time ni .models.py da created_tile deb yozilgan!!!!!!!!!!!!!!!!!!!!
    prepopulated_fields = {'slug': ('title' ,)}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_time']


admin.site.register(Contact)

