from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),

    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view()),

    path('reviews/', views.ReviewViewSet.as_view({
        'get': 'list','post': 'create'
    })),
    path('reviews/<int:id>/', views.ReviewViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),

    path('products/reviews/', views.product_reviews_api_view),
]