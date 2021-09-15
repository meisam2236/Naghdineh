from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'stock']
    search_fields = ['title', 'content', 'category']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'date_time', 'category', 'wallet_name']
    search_fields = ['title', 'category', 'wallet_name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class WalletAdmin(admin.ModelAdmin):
    list_display = ['title', 'stock']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Wallet, WalletAdmin)