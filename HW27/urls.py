
from django.contrib import admin
from django.urls import path

from ads import views
from ads.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main),
    path('cat/', CategoryView.as_view(), name='cat'),
    path('ads/', AdsView.as_view(), name='ads'),
    path('cat/<int:pk>', CategoryDetailView.as_view(), name='cat_detail'),
    path('ads/<int:pk>', AdsDetailView.as_view(), name='ads_detail'),
    path('cat/create/', CategoryCreateView.as_view(), name='create_cat'),
    path('ads/create/', AdsCreateView.as_view(), name='create_ads'),
    path('ads/<int:pk>/update', AdsUpdateView.as_view(), name='update_ads'),
    path('cat/<int:pk>/update', CategoryUpdateView.as_view(), name='update_ads'),
    path('cat/<int:pk>/delete', CategoryDeleteView.as_view(), name='delete_cat'),
    path('ads/<int:pk>/delete', AdsDeleteView.as_view(), name='delete_ads'),
]
