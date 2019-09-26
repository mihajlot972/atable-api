from django.urls import path, include
from .views import (
    CreateUserView, 
    GetAllUsersView,
    GetCurrentUser,
)
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/register/', CreateUserView.as_view(), name='register'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', GetAllUsersView.as_view(), name='homescreen'),
    path('api/user/<int:id>/', GetCurrentUser.as_view(), name='get_user'),
]