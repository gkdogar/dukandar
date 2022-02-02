from rest_framework import serializers
from django.contrib.auth.models import User
from shopkeeper.models.models import *



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'password2', 'first_name', 'last_name','user_type','address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        user.set_password(password)
        user.save()
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(many=False, read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ShopkeeperSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    emp_id = serializers.StringRelatedField(many=False)
    class Meta:
        model = Shopkeeper
        fields = '__all__'
    
class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField(many=False)
    sub_cat = serializers.StringRelatedField(many=False)
    class Meta:
        model = Product
        fields = '__all__'
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'