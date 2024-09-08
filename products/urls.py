from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()  # 라우터 생성
router.register(r'products', ProductViewSet)  # 'products' 엔드포인트에 ProductViewSet 등록

urlpatterns = [
    path('', include(router.urls)),  # 라우터에서 생성된 URL 패턴 포함
]
