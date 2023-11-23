from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)

'''
ban đầu nếu sử dụng câu lệnh admin.site.register(Cart,CartItem) thì sẽ dẫn đến lỗi AttributeError: 'CartItem' object has no attribute 'urls' . 
tuy nhiên khi tách dòng như cú pháp trên lại không xuất hiện lôic. Giải thích nguyên nhana xảy ra điều này?
'''
