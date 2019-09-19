from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.safestring import mark_safe

from common.models import Product, Review, Transaction, Vendor

class InventoryInline(admin.TabularInline):
    model = Product.vendors.through

class ProductAdmin(admin.ModelAdmin):
    search_fields   = ('name', 'vendors__name',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    inlines         = [
        InventoryInline,
    ]
admin.site.register(Product, ProductAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display    = ('created_at', 'vendor_link', 'transaction_link', 'product_link',)
    list_filter     = ('created_at',)
    search_fields   = ('id', 'vendor__name', 'transaction__customer_email', 'transaction__customer_phone', 'product__name',)
    readonly_fields = ('id', 'analytics_id', 'sentiment_analysis', 'created_at', 'updated_at',)

    def vendor_link(self, obj):
        return mark_safe(f'<a href="{reverse("admin:common_vendor_change", args=(obj.vendor.pk,))}">{obj.vendor}</a>')
    vendor_link.short_description = 'vendor'

    def transaction_link(self, obj):
        return mark_safe(f'<a href="{reverse("admin:common_transaction_change", args=(obj.transaction.pk,))}">{obj.transaction}</a>')
    transaction_link.short_description = 'transaction'

    def product_link(self, obj):
        return mark_safe(f'<a href="{reverse("admin:common_product_change", args=(obj.product.pk,))}">{obj.product}</a>')
    product_link.short_description = 'product'
admin.site.register(Review, ReviewAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display        = ('created_at', 'customer_contact', 'vendor_link',)
    list_filter         = ('review_requests_sent',)
    search_fields       = ('id', 'customer_email', 'customer_phone', 'products__name', 'vendor__id', 'vendor__name',)
    readonly_fields     = ('id', 'review_requests_sent', 'created_at', 'updated_at',)
    filter_horizontal   = ('products',)

    def vendor_link(self, obj):
        return mark_safe(f'<a href="{reverse("admin:common_vendor_change", args=(obj.vendor.pk,))}">{obj.vendor}</a>')
    vendor_link.short_description = 'vendor'
admin.site.register(Transaction, TransactionAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display    = ('__str__', 'integrations_type', 'integrations_id',)
    list_filter     = ('integrations_type',)
    search_fields   = ('id', 'name', 'integrations_type', 'integrations_id',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    inlines         = [
        InventoryInline,
    ]
admin.site.register(Vendor, VendorAdmin)
