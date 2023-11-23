from django.contrib import admin
from .models import Product 
# Register your models here.

class ProductAdmin(admin.ModelAdmin): 
    list_display=('product_name','slug','description','price','stock','category','created_date','modified_date','is_available')
    prepopulated_fields ={'slug': ('product_name',)} # set prepopulated_fields to a dictionary mapping field names to the fields, it shold prepopulate from here

admin.site.register(Product, ProductAdmin)
