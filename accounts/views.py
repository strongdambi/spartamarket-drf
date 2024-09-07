from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import User
from .serializers import SignUpSerializer, SignInSerializer, ProfileSerializer, ProfileUpdateSerializer
from .validators import validate_user_data, validate_profile_update, validate_password_change, validate_delete_account, validate_refresh_token


class AccountView(APIView):
    #회원가입 로직
    def post(self, request): 
        is_valid, error_message = validate_user_data(request.data)
        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

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
        )

        serializer = SignUpSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 계정 삭제 로직
    def delete(self, request): 
        user = request.user
        password = request.data.get('password')
        try:
            validate_delete_account(user, password)
        except ValidationError as e:
            return Response({"error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({"success": "계정이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


class SignInView(APIView):
    def post(self, request):
        #클라이언트로부터 username과 password를 받음
        username = request.data.get('username')
        password = request.data.get('password')

        # 사용자 인증
        user = authenticate(username=username, password=password)

        # 인증 실패: 401 반환
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
            # 검증 함수 호출
            refresh_token = validate_refresh_token(refresh_token_str)
        except ValidationError as e:
            return Response({"error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

        # 리프레시 토큰 블랙리스트 처리
        refresh_token.blacklist()
        return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    # 프로필 조회 로직
    def get(self, request, username):
        if request.user.username != username:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
    
    # 프로필 수정 로직
    def put(self, request, username):
        # 사용자 권한 및 이메일 중복 검증 호출
        is_valid, error_messages = validate_profile_update(request.user, username, request.data.get('email'))

        if not is_valid:
            return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 정보 가져오기 (권한 검증 통과 후)
        user = get_object_or_404(User, username=username)

        # 사용자 정보 업데이트
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # print("뷰가 왜 호출이 안되냐고!!!!")
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')

        try:
            # 패스워드 변경 검증 로직 호출
            validate_password_change(user, current_password, new_password, new_password_confirm)
        except ValidationError as e:
            return Response({"error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 저장
        user.set_password(new_password)
        user.save()

        return Response({"success": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)