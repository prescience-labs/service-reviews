from django.urls import path
from v1 import views

urlpatterns = [
    path('/absa-events', views.ABSAEventList.as_view(), name='event_list'),

    path('/products', views.ProductList.as_view(), name='product_list'),
    path('/products/<str:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('/products/<str:pk>/vendors', views.ProductVendorList.as_view(), name='product_vendor_list'),
    path('/products/<str:pk>/reviews', views.ProductReviewList.as_view(), name='product_review_list'),
    path('/products/<str:pk>/transactions', views.ProductTransactionList.as_view(), name='product_transaction_list'),

    path('/reviews', views.ReviewList.as_view(), name='review_list'),
    path('/reviews/<str:pk>', views.ReviewDetail.as_view(), name='review_detail'),
    path('/reviews/<str:pk>/absa-events', views.ReviewABSAEventList.as_view(), name='review_absa_event_list'),

    path('/transactions', views.TransactionList.as_view(), name='transaction_list'),
    path('/transactions/comprehensive', views.UpsertTransactionComprehensive.as_view(), name='transaction_comprehensive'),
    path('/transactions/<str:pk>', views.TransactionDetail.as_view(), name='transaction_detail'),
    path('/transactions/<str:pk>/products', views.TransactionProductList.as_view(), name='transaction_product_list'),

    path('/vendors', views.VendorList.as_view(), name='vendor_list'),
    path('/vendors/<str:pk>', views.VendorDetail.as_view(), name='vendor_detail'),
    path('/vendors/<str:pk>/products', views.VendorProductList.as_view(), name='vendor_product_list'),
]
