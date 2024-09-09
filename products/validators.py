from rest_framework.response import Response
from rest_framework import status

def product_update_author(request, product):
    if product.user != request.user:
        return Response({"error": "작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    return None


def product_delete_author(request, product):
    if product.user != request.user:
        return Response({"error": "작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    return None
