from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, SignInView, SignOutView, ProfileView

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('login/', SignInView.as_view(), name='signin'),
    path('logout/', SignOutView.as_view(), name='signout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
]
