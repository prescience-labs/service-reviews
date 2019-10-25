from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.safestring import mark_safe

from common.models import ABSAEvent, Product, Review, Transaction, Vendor

base_readonly_fields = ('id', 'created_at', 'updated_at',)

class InventoryInline(admin.TabularInline):
    model = Product.vendors.through

class ProductAdmin(admin.ModelAdmin):
    search_fields   = ('name', 'vendors__name',)
    readonly_fields = base_readonly_fields
    inlines         = [
        InventoryInline,
    ]
admin.site.register(Product, ProductAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display    = ('created_at', 'vendor_link',)
    list_filter     = ('created_at',)
    ordering        = ('-created_at',)
    search_fields   = ('id', 'vendor__name', 'transaction__customer_email', 'transaction__customer_phone', 'product__name',)
    readonly_fields = base_readonly_fields + ('analytics_id', 'sentiment_analysis',)

    def vendor_link(self, obj):
        return mark_safe(f'<a href="{reverse("admin:common_vendor_change", args=(obj.vendor.pk,))}">{obj.vendor}</a>')
    vendor_link.short_description = 'vendor'
admin.site.register(Review, ReviewAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display        = ('created_at', 'customer_contact', 'vendor_link',)
    list_filter         = ('review_requests_sent',)
    ordering            = ('-created_at',)
    search_fields       = ('id', 'customer_email', 'customer_phone', 'products__name', 'vendor__id', 'vendor__name',)
    readonly_fields     = base_readonly_fields + ('review_requests_sent',)
    filter_horizontal   = ('products',)

    def vendor_link(self, obj):
        return mark_safe(f'<a href="{reverse("admin:common_vendor_change", args=(obj.vendor.pk,))}">{obj.vendor}</a>')
    vendor_link.short_description = 'vendor'
admin.site.register(Transaction, TransactionAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display    = ('__str__', 'integrations_type', 'integrations_id', 'send_comms_to_customers',)
    list_filter     = ('integrations_type', 'send_comms_to_customers',)
    search_fields   = ('id', 'name', 'integrations_type', 'integrations_id',)
    readonly_fields = base_readonly_fields
    inlines         = [
        InventoryInline,
    ]
admin.site.register(Vendor, VendorAdmin)

class ABSAEventAdmin(admin.ModelAdmin):
    list_display    = ('__str__', 'event_type', 'score',)
    list_filter     = ('event_type',)
    readonly_fields = base_readonly_fields + ('review',)
admin.site.register(ABSAEvent, ABSAEventAdmin)
