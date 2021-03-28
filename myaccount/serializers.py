from django.contrib.auth.models import User
from rest_framework import serializers

from myaccount.models import UserDetail
from utils.utils import getattr_recursive


class AuthUserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = ('username', 'password')

class UserSerializer( serializers.ModelSerializer ):
    auth_id = serializers.CharField(read_only=True, source='auth_user.id')
    username = serializers.CharField(read_only=True, source='auth_user.username')
    email = serializers.CharField(read_only=True, source='auth_user.email')
    name = serializers.CharField(read_only=True, source='auth_user.first_name')
    last_name = serializers.CharField(read_only=True, source='auth_user.last_name')
    #image = serializers.SerializerMethodField()

    class Meta:
        model = UserDetail
        fields = ('auth_id', 'username','email','mobile', 'name', 'last_name')

    #def get_image(self, obj):
    #    return getattr_recursive(obj, ['image', 'url'])

class UserNameSerializer(serializers.ModelSerializer):
    fname = serializers.CharField(read_only=True, source='auth_user.first_name')
    lname = serializers.CharField(read_only=True, source='auth_user.last_name')

    class Meta:
        model = UserDetail
        fields = ('id', 'fname', 'lname')
