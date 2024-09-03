from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .setializers import AccountSerializer


class AccountAPIView(APIView):
    def post(self, request):
        password = request.data.get('password')
        password_check = request.data.get('password_check')
        
        # create_user() 메서드에 비밀번호 확인 과정이 없어서 추가
        
        if password != password_check:
            error_message = {"error": "비밀번호가 일치하지 않습니다."}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
