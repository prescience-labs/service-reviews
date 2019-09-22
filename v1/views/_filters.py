from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from common.models import Product, Review, Vendor

class ProductFilter(filters.FilterSet):
    vendor_product_id       = filters.CharFilter(field_name='inventory__vendor_product_id', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy `vendor_product_id` search'))
    vendor_product_id_exact = filters.CharFilter(field_name='inventory__vendor_product_id', lookup_expr='exact', help_text=_('Exact `vendor_product_id` search'))
    name                    = filters.CharFilter(field_name='name', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy `name` search'))
    name_exact              = filters.CharFilter(field_name='name', lookup_expr='exact', help_text=_('Exact `name` search'))

    class Meta:
        model   = Product
        fields  = [
            'vendor_product_id',
            'vendor_product_id_exact',
            'name',
            'name_exact',
        ]

class ReviewFilter(filters.FilterSet):
    text    = filters.CharFilter(field_name='text', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy text search'))
    before  = filters.DateFilter(field_name='created_at', lookup_expr='lte', help_text=_('**Exclusive** before date (YYYY-MM-DD)'))
    after   = filters.DateFilter(field_name='created_at', lookup_expr='gte', help_text=_('**Inclusive** after date (YYYY-MM-DD)'))

    class Meta:
        model   = Review
        fields  = [
            'text',
        ]

class VendorFilter(filters.FilterSet):
    integrations_type       = filters.CharFilter(field_name='integrations_type', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy `integrations_type` search'))
    integrations_type_exact = filters.CharFilter(field_name='integrations_type', lookup_expr='exact', help_text=_('Exact `integrations_type` search'))
    integrations_id         = filters.CharFilter(field_name='integrations_id', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy `integrations_id` search'))
    integrations_id_exact   = filters.CharFilter(field_name='integrations_id', lookup_expr='exact', help_text=_('Exact `integrations_id` search'))
    name                    = filters.CharFilter(field_name='name', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy `name` search'))
    name_exact              = filters.CharFilter(field_name='name', lookup_expr='exact', help_text=_('Exact `name` search'))

    class Meta:
        model   = Vendor
        fields  = [
            'integrations_type',
            'integrations_type_exact',
            'integrations_id',
            'integrations_id_exact',
            'name',
            'name_exact',
        ]
