from rest_framework import serializers
from django.contrib.auth.models import User
from shopkeeper.models.models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name')
