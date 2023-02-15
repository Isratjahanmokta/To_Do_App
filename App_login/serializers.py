from rest_framework import serializers
from .models import Task, UserSignUp
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Task.objects.create(**validated_data)

class userSerializers(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = UserSignUp
        fields = [
                'first_name', 
                'last_name', 
                'username',
                'password',
                'email',
                'address',
                'image']
    def create(self, validated_data):
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.save()
        user.set_password(validated_data.pop("password"))
        user.save()

        instance = UserSignUp.objects.create(
            user=user,
            **validated_data,
        )

        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
 
        try:
            RefreshToken(self.token).blacklist()

        except TokenError as ex:
            raise exceptions.AuthenticationFailed(ex)