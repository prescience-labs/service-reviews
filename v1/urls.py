from django.urls import path
from v1 import views

urlpatterns = [
    path('/reviews',            views.ReviewList.as_view(),     name='review_list'),
    path('/reviews/<str:id>',   views.ReviewDetail.as_view(),   name='review_detail'),
]
