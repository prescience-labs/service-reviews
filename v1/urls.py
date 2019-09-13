from django.urls import path
from v1 import views

urlpatterns = [
    path('/products', views.ProductList.as_view(), name='product_list'),
    path('/products/<str:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('/reviews', views.ReviewList.as_view(), name='review_list'),
    path('/reviews/<str:pk>', views.ReviewDetail.as_view(), name='review_detail'),
    path('/vendors', views.VendorList.as_view(), name='vendor_list'),
    path('/vendors/<str:pk>', views.VendorDetail.as_view(), name='vendor_detail'),
]
