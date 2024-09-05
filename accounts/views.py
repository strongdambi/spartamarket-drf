from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import User
from .serializers import SignUpSerializer, SignInSerializer, ProfileSerializer
from .validators import validate_user_data

class SignUpView(APIView):
    def post(self, request):
        # 사용자 입력 데이터 검증
        is_valid, error_message = validate_user_data(request.data)

        # 오류가 있으면 모든 오류 메시지를 반환
        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 생성 
        user = User.objects.create_user(
            username=request.data.get('username'),
            password=request.data.get('password'),
            email=request.data.get('email'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            nickname=request.data.get('nickname'),
            date_of_birth=request.data.get('date_of_birth'),
            gender=request.data.get('gender', ''),
            bio=request.data.get('bio', '')
            # **requset.data
        )

        # 생성된 사용자 직렬화 및 응답 반환
        serializer = SignUpSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SignInView(APIView):
    def post(self, request):
        #클라이언트로부터 username과 password를 받음
        username = request.data.get('username')
        password = request.data.get('password')

        # 사용자 인증
        user = authenticate(username=username, password=password)

        #인증 실패: 401 반환
        if not user:
            return Response({"error": "유저네임 또는 비밀번호가 올바르지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 인증 성공: 사용자 정보 직렬화
        serializer = SignInSerializer(user)
        res_data = serializer.data

        # 토큰
        refresh = RefreshToken.for_user(user) # 리프레시 토큰 생성
        res_data["access_token"] = str(refresh.access_token) 
        res_data["refresh_token"] = str(refresh)
        return Response(res_data)


class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token_str = request.data.get("refresh_token")
        try:
            # 리프레시 토큰 객체 생성 및 유효성 검사
            refresh_token = RefreshToken(refresh_token_str)
        except TokenError as e:
            # 블랙리스트에 이미 등록된 경우 예외 처리
            return Response({"msg": "This token is already blacklisted."}, status=400)

        # 블랙리스트에 추가
        refresh_token.blacklist()
        return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        # 요청한 username이 일치하는지 확인
        if request.user.username != username:
            return Response(
                {"error": "권한이 없어 프로필을 조회할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)