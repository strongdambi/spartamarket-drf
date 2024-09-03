from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AccountAPIView

urlpatterns = [
    path('signup/', AccountAPIView.as_view(), name='signup'),
    path('signin/', TokenObtainPairView.as_view(), name='toekn_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
