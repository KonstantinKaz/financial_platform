from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/drf-auth/', include('rest_framework.urls')),
    # path('api/women/', WomenAPIList.as_view()),
    # path('api/women/<int:pk>/', WomenAPIUpdate.as_view()),
    # path('api/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),
    path('api/auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/', include('finance.urls')),
]
