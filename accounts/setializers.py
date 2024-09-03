from rest_framework import serializers
from .models import User


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 
            'password', 
            'email', 
            'name', 
            'nickname', 
            'date_of_birth', 
            'gender', 
            'bio'
            ]
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data['email'],
            name = validated_data.get('name', ''),
            nickname = validated_data.get('nickname', ''),
            date_of_birth = validated_data.get('date_of_birth'),
            gender = validated_data.get('gender', ''),
            bio = validated_data.get('bio', '')
        )
        return user