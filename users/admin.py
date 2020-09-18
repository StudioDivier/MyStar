from django.contrib import admin
from .models import Stars, Customers, Categories


class StarsAdmin(admin.ModelAdmin):
    list_display = ('username', 'rating', 'cat_name_id')
    list_filter = ('rating', 'cat_name_id')
    fieldsets = (
        ('Инфорамция о Звезде',{
            'fields': ('username', ('first_name', 'last_name'))
        }),
        ('Коммерческая информация', {
            'fields': ('cat_name_id', 'price', 'rating')
        }),
    )


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_of_birth')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name',)


admin.site.register(Categories, CategoryAdmin)
admin.site.register(Stars, StarsAdmin)
admin.site.register(Customers, CustomersAdmin)

