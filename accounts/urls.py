# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AccountView, SignInView, SignOutView, ProfileView, PasswordChangeView

app_name = "accounts"
urlpatterns = [
    path('', AccountView.as_view()),  # 회원가입(POST) & 계정삭제(DELETE)
    path('login/', SignInView.as_view()),
    path('logout/', SignOutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('password/', PasswordChangeView.as_view()),
    path('<str:username>/', ProfileView.as_view()),  # 프로필 조회(GET) & 프로필 정보 변경(PUT)
]