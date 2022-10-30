from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads import views
from ads.views import *

router = SimpleRouter()
router.register('location', LocationViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.main),
                  path('cat/', CategoryView.as_view(), name='cat'),
                  path('ads/', AdsView.as_view(), name='ads'),
                  path('cat/<int:pk>/', CategoryDetailView.as_view(), name='cat_detail'),
                  path('ads/<int:pk>/', AdsDetailView.as_view(), name='ads_detail'),
                  path('cat/create/', CategoryCreateView.as_view(), name='create_cat'),
                  path('ads/create/', AdsCreateView.as_view(), name='create_ads'),
                  path('ads/update/<int:pk>/', AdsUpdateView.as_view(), name='update_ads'),
                  path('cat/update/<int:pk>/', CategoryUpdateView.as_view(), name='update_ads'),
                  path('cat/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_cat'),
                  path('ads/delete/<int:pk>/', AdsDeleteView.as_view(), name='delete_ads'),
                  path('ads/<int:pk>/upload_image/', AdUpdateImageView.as_view(), name='upload_image'),
                  path('user/create/', UserCreateView.as_view()),
                  path('user/', UserListView.as_view()),
                  path('user/delete/<int:pk>/', UserDeleteView.as_view()),
                  path('user/update/<int:pk>/', UserUpdateView.as_view()),
                  path('user/<int:pk>/', UserDetailView.as_view()),
                  path('token/', TokenObtainPairView.as_view()),
                  path('token/refresh/', TokenRefreshView.as_view()),
                  path('selection/<int:pk>/', SelectionDetailView.as_view()),
                  path('selection/create/', SelectionCreateView.as_view()),
                  path('selection/delete/', SelectionDeleteView.as_view()),
                  path('selection/update/<int:pk>/', SelectionUpdateView.as_view()),
                  path('selection/', SelectionListView.as_view()),
                  path('login/', views.obtain_auth_token), # не подключается к from ads import views ????
                  path('logout/', Logout.as_view()),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
