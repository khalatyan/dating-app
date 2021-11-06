from rest_framework import serializers

from core.models import User, Estimation
from core.models import ESTIMATION
from utils.image_functions import watermark_photo


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    replay_password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4),
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    additional_fields = ['replay_password']

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'sex', 'user_photo', 'password', 'replay_password'
                  ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        replay_password = attrs.get('replay_password', '')
        if password != replay_password:
            raise serializers.ValidationError(
                {'replay_password': ('Введенные пароли не совпадают')})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Пользователь с такой почтой уже зарегистрирован')})
        return super().validate(attrs)

    def create(self, validated_data):
        for key in self.additional_fields:
            del validated_data[key]
        if validated_data['user_photo']:
            validated_data['user_photo'] = watermark_photo(validated_data['user_photo'], validated_data['email'])
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['email', 'password']


class EstimationSerializer(serializers.ModelSerializer):
    jwt = serializers.CharField(
        max_length=115, min_length=115)

    class Meta:
        model = Estimation
        fields = ['jwt', 'estimation']
