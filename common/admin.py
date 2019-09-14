from django.contrib import admin

from common.models import Product, Review, Transaction, Vendor

class InventoryInline(admin.TabularInline):
    model = Product.vendors.through

class ProductAdmin(admin.ModelAdmin):
    search_fields   = ('name', 'vendors__name',)
    readonly_fields = ('created_at', 'updated_at',)
    inlines         = [
        InventoryInline,
    ]
admin.site.register(Product, ProductAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display    = ('created_at', 'vendor', 'transaction', 'product',)
    list_filter     = ('created_at',)
    search_fields   = ('id', 'vendor__name', 'transaction__customer_email', 'transaction__customer_phone', 'product__name',)
    readonly_fields = ('sentiment_analysis', 'created_at', 'updated_at',)
admin.site.register(Review, ReviewAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display        = ('created_at', 'customer_contact',)
    search_fields       = ('id', 'customer_email', 'customer_phone', 'products__name',)
    readonly_fields     = ('created_at', 'updated_at',)
    filter_horizontal   = ('products',)
admin.site.register(Transaction, TransactionAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display    = ('__str__', 'integrations_type', 'integrations_id',)
    list_filter     = ('integrations_type',)
    search_fields   = ('id', 'name', 'integrations_type', 'integrations_id',)
    readonly_fields = ('created_at', 'updated_at',)
    inlines         = [
        InventoryInline,
    ]
admin.site.register(Vendor, VendorAdmin)
