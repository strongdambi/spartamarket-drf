from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .validators import product_update_author, product_delete_author

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 조회는 누구나, 등록/수정/삭제는 로그인 필요
    filter_backends = [filters.SearchFilter]  # 필터링 기능 추가
    search_fields = ['title', 'content', 'user__username']  # 필터링 가능 필드

    # 로그인한 사용자를 user 필드에 자동으로 넣기
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        product = self.get_object()  # 수정할 상품
        author_check = product_update_author(request, product)  # 작성자 검증
        if author_check:
            return author_check  # 작성자가 아니면 에러
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()  # 삭제할 상품 가져오기
        author_check = product_delete_author(request, product)  # 작성자 검증
        if author_check:
            return author_check  # 작성자가 아니면 에러 반환
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # get_permissions 메서드를 오버라이딩하여 액션별로 권한을 다르게 설정
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]  # 관리자만 접근 가능
        else:
            self.permission_classes = [AllowAny]  # 조회 관련 액션은 누구나 접근 가능
        return super().get_permissions()
