from django.contrib import admin
from django.urls import path, include
from . import swager

urlpatterns = [
    path('admin/',admin.site.urls),
    path('api/v1/product/',include('product.urls')),
    path('api/v1/users/',include('users.urls')),

]

urlpatterns += swager.urlpatterns