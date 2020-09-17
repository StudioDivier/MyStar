from django.contrib import admin
from .models import Stars, Customers, Categories, Ratings


class StarsAdmin(admin.ModelAdmin):
    pass


class CustomersAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Categories, CategoryAdmin)
admin.site.register(Stars, StarsAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Ratings)
