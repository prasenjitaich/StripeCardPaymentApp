from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    serializer to handle turning our `User` object into
    something that can be JSONified and sent to the client
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """
        Function is used to create user object with serializer.
        :param validated_data: keep all user related data.
        :return: user object.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Function is used for the update user information.
        :param instance: user object instance
        :param validated_data: new info passed in request.
        :return: user object.
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'created_on',
                  'modified_on')
