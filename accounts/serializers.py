from rest_framework import serializers
from .models import User

# 부모 시리얼라이저
class MyBaseSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # 공통 필드

# 회원가입 시리얼라이저
class SignUpSerializer(MyBaseSerializer):
    password = serializers.CharField(write_only=True)

    class Meta(MyBaseSerializer.Meta):
        fields = MyBaseSerializer.Meta.fields + ['password', 'nickname', 'date_of_birth', 'gender', 'bio']

# 로그인 시리얼라이저
class SignInSerializer(MyBaseSerializer):
    class Meta(MyBaseSerializer.Meta):
        fields = MyBaseSerializer.Meta.fields

# 프로필 조회 시리얼라이저
class ProfileSerializer(MyBaseSerializer):
    class Meta(MyBaseSerializer.Meta):
        fields = MyBaseSerializer.Meta.fields + ['nickname', 'date_of_birth', 'gender', 'bio']

# 프로필 업데이트 시리얼라이저
class ProfileUpdateSerializer(MyBaseSerializer):
    class Meta(MyBaseSerializer.Meta):
        fields = ['email', 'first_name', 'last_name', 'nickname', 'date_of_birth', 'gender', 'bio']
