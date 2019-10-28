from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from common.models import ABSAEvent, Product, Review, Transaction, Vendor

class ABSAEventFilter(filters.FilterSet):
    before      = filters.DateFilter(field_name='created_at', lookup_expr='lte', help_text=_('**Exclusive** created before date (YYYY-MM-DD)'))
    after       = filters.DateFilter(field_name='created_at', lookup_expr='gte', help_text=_('**Inclusive** created after date (YYYY-MM-DD)'))
    term        = filters.CharFilter(field_name='term', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy `term` search'))
    variant     = filters.CharFilter(field_name='variant', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy `variant` search'))
    event_type  = filters.CharFilter(field_name='event_type', lookup_expr='exact', help_text=_('Exact event type'))

class ProductFilter(filters.FilterSet):
    before                  = filters.DateFilter(field_name='created_at', lookup_expr='lte', help_text=_('**Exclusive** created before date (YYYY-MM-DD)'))
    after                   = filters.DateFilter(field_name='created_at', lookup_expr='gte', help_text=_('**Inclusive** created after date (YYYY-MM-DD)'))
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
    before  = filters.DateFilter(field_name='created_at', lookup_expr='lte', help_text=_('**Exclusive** created before date (YYYY-MM-DD)'))
    after   = filters.DateFilter(field_name='created_at', lookup_expr='gte', help_text=_('**Inclusive** created after date (YYYY-MM-DD)'))
    text    = filters.CharFilter(field_name='text', lookup_expr='icontains', help_text=_('Case-insensitive fuzzy text search'))

    class Meta:
        model   = Review
        fields  = [
            'text',
        ]

class TransactionFilter(filters.FilterSet):
    before                      = filters.DateFilter(field_name='created_at', lookup_expr='lte', help_text=_('**Exclusive** created before date (YYYY-MM-DD)'))
    after                       = filters.DateFilter(field_name='created_at', lookup_expr='gte', help_text=_('**Inclusive** created after date (YYYY-MM-DD)'))
    vendor_transaction_id_exact = filters.CharFilter(field_name='vendor_transaction_id', lookup_expr='exact', help_text='Exact `vendor_transaction_id` search')
    customer_email              = filters.CharFilter(field_name='customer_email', lookup_expr='icontains', help_text='Case-insensitive fuzzy `customer_email` search')
    customer_email_exact        = filters.CharFilter(field_name='customer_email', lookup_expr='exact', help_text='Exact `customer_email` search')
    customer_phone              = filters.CharFilter(field_name='customer_phone', lookup_expr='icontains', help_text='Case-insensitive fuzzy `customer_phone` search')
    customer_phone_exact        = filters.CharFilter(field_name='customer_phone', lookup_expr='exact', help_text='Exact `customer_phone` search')
    review_requests_sent_exact  = filters.NumberFilter(field_name='review_requests_sent', lookup_expr='exact', help_text='Exact count lookup on `review_requests_sent`')

    class Meta:
        model   = Transaction
        fields  = [
            'vendor_transaction_id_exact',
            'customer_email',
            'customer_email_exact',
            'customer_phone',
            'customer_phone_exact',
            'review_requests_sent_exact',
        ]

class VendorFilter(filters.FilterSet):
    before                  = filters.DateFilter(field_name='created_at', lookup_expr='lte', help_text=_('**Exclusive** created before date (YYYY-MM-DD)'))
    after                   = filters.DateFilter(field_name='created_at', lookup_expr='gte', help_text=_('**Inclusive** created after date (YYYY-MM-DD)'))
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
