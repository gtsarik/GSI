from django.contrib import admin

from customers.models import (Category, ShelfData, DataSet)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ShelfDataAdmin(admin.ModelAdmin):
    list_display = ('category', 'attribute_name', 'root_filename', 'units',)
    search_fields = ['category', 'attribute_name', 'root_filename',]
    list_filter = ('category', 'attribute_name', 'root_filename',)


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'results_directory', 'get_attribute_name', 'get_root_filename',)
    search_fields = ['name', 'description', 'get_attribute_name',]
    list_filter = ('name', 'description', 'shelf_data__attribute_name', 'shelf_data__root_filename',)

    def get_attribute_name(self, obj):
        return obj.shelf_data.attribute_name

    def get_root_filename(self, obj):
        return obj.shelf_data.root_filename

    get_attribute_name.short_description = 'Atribute Name'
    get_root_filename.short_description = 'Root Filename'


admin.site.register(Category, CategoryAdmin)
admin.site.register(ShelfData, ShelfDataAdmin)
admin.site.register(DataSet, DataSetAdmin)