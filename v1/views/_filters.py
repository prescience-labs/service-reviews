from django_filters import rest_framework as filters

from common.models import Product, Vendor

class ProductFilter(filters.FilterSet):
    vendor_product_id       = filters.CharFilter(field_name='inventory__vendor_product_id', lookup_expr='icontains')
    vendor_product_id_exact = filters.CharFilter(field_name='inventory__vendor_product_id', lookup_expr='exact')
    name                    = filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_exact              = filters.CharFilter(field_name='name', lookup_expr='exact')

    class Meta:
        model   = Product
        fields  = [
            'vendor_product_id',
            'vendor_product_id_exact',
            'name',
            'name_exact',
        ]

class VendorFilter(filters.FilterSet):
    integrations_type       = filters.CharFilter(field_name='integrations_type', lookup_expr='icontains')
    integrations_type_exact = filters.CharFilter(field_name='integrations_type', lookup_expr='exact')
    integrations_id         = filters.CharFilter(field_name='integrations_id', lookup_expr='icontains')
    integrations_id_exact   = filters.CharFilter(field_name='integrations_id', lookup_expr='exact')
    name                    = filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_exact              = filters.CharFilter(field_name='name', lookup_expr='exact')

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
