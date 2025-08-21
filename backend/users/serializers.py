from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The passwords dont match")
        validate_password(data['password'])
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The passwords dont match")
        validate_password(data['password'])
        return super().validate(data)
    
    def update(self, instance, validated_data):
        if instance.check_password(validated_data['password']):
            raise serializers.ValidationError({
                "message": "The password must be different from the current one"
            })
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
