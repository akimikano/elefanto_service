from rest_framework import serializers
from apps.user.models import User
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"})
    re_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        'password_mismatch': 'Passwords are not same.'
    }

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 're_password'
        )

    def to_representation(self, instance):
        return UserSerializer(instance).data

    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)

        user = User(**attrs)

        try:
            validate_password(attrs['password'], user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail('password_mismatch')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if settings.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            user.save(update_fields=['is_active'])
        return user
