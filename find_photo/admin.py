from django.contrib import admin
from .models import *
# Register your models here.


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image',)
    list_display_links = ('id', 'image')
    search_fields = ()
    readonly_fields = ('id',)
    ordering = ()
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Images, ImagesAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'date_of_add',)
    list_display_links = ('id', 'image')
    search_fields = ()
    readonly_fields = ('id', 'date_of_add')
    ordering = ()
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Gallery, GalleryAdmin)


class GroupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_of_add',)
    list_display_links = ('title', 'id',)
    search_fields = ('title',)
    readonly_fields = ('id', 'date_of_add')
    ordering = ()
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Groups, GroupsAdmin)
