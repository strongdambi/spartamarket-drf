from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer
from .validators import product_update_author, product_delete_author

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 조회는 누구나, 등록/수정/삭제는 로그인 필요
    filter_backends = [filters.SearchFilter]  # 필터링 기능 추가
    search_fields = ['title', 'content', 'user__username']  # 제목, 내용, 사용자 이름으로 검색 가능

    # 로그인한 사용자를 user 필드에 자동으로 넣기
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        product = self.get_object()  # 수정할 상품 가져오기
        author_check = product_update_author(request, product)  # 작성자 검증
        if author_check:
            return author_check  # 작성자가 아니면 에러 반환
        return super().update(request, *args, **kwargs)  # 기본 수정 로직 수행

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()  # 삭제할 상품 가져오기
        author_check = product_delete_author(request, product)  # 작성자 검증
        if author_check:
            return author_check  # 작성자가 아니면 에러 반환
        return super().destroy(request, *args, **kwargs)  # 기본 삭제 로직 수행
