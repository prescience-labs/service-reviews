from django.urls import path
from v1 import views

urlpatterns = [
    path('/reviews', views.ReviewList.as_view(), name='review_list'),
    path('/reviews/<str:pk>', views.ReviewDetail.as_view(), name='review_detail'),
    path('/review_requests', views.ReviewRequestList.as_view(), name='review_request_list'),
    path('/review_requests/<str:pk>', views.ReviewRequestDetail.as_view(), name='review_request_detail'),
]
