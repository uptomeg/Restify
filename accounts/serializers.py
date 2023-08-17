from rest_framework.serializers import ModelSerializer, CharField
from .models import User
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirm', 'avatar'
                  , 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id', )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data.get('avatar', None),
            phone_number=validated_data.get('phone_number', None)
        )
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        user.set_password(password)
        user.save()
        return user


class UpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)
    password_confirm = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'avatar', 'password', 'password_confirm']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data.get('avatar', None),
            phone_number=validated_data.get('phone_number', None)
        )
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        user.set_password(password)
        return user


    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)

        if password != password_confirm:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        if password and password_confirm and password == password_confirm:
            instance.set_password(password)
        instance.save()

        return instance