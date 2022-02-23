from rest_framework import serializers
from django.contrib.auth.models import User
from shopkeeper.models.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name','phone_no','address','city', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'address': {'required': True},
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
        fields = ['user','target_assign','target_achieved','area_designated','description']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(many=False, read_only=True)
    email = serializers.CharField(style={'input_type': 'email'}, write_only=True)
    first_name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    last_name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    address = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    city = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    phone_no = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Customer
        fields =['email','password', 'password2','first_name','last_name',  'address', 'city','phone_no','user']
        # fields = '__all__'
        # depth = 1
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'address': {'write_only': True},
            'shop_name': {'required': True},
            'phone_no': {'required': True},

        }


class ShopkeeperSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(many=False, read_only=True)
    email = serializers.CharField(style={'input_type': 'email'}, write_only=True)
    first_name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    last_name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    address = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    city = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    phone_no = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    # emp_id = EmployeeSerializer(many=False, read_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Shopkeeper
        fields = ['id','user','email', 'first_name', 'last_name','address','city','phone_no', 'emp_id', 'shop_name','description', 'latitude', 'longitude',
                  'password', 'password2']
        # fields = '__all__'
        # depth = 1

    extra_kwargs = {
        'first_name': {'required': True},
        'password': {'write_only': True},
        'address': {'write_only': True},
        'shop_name': {'required': True},
        'phone_no': {'required': True},
        'description': {'required': True},
        'latitude': {'required': True},
        'longitude': {'required': True},
        'emp_id':{"required":True}
    }


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        # fields = '__all__'
        fields = ['id', 'name', 'description','meta_keywords','meta_description','image']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        # fields = '__all__'
        fields = ['id','parent', 'name', 'description', 'meta_keywords', 'meta_description', 'image']
        # depth = 1



class ProductSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField(many=False)
    sub_cat = serializers.StringRelatedField(many=False)

    class Meta:
        model = Product
        fields = '__all__'

class ProductOrderSerializer(serializers.ModelSerializer):
   
    # product = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    # amount = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    # quantity = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    class Meta:
        model = ProductOrder
        fields = '__all__'
      

class OrderSerializer(serializers.ModelSerializer):
   
    # product = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    # amount = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    # quantity = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    class Meta:
        model = Order
        fields ='__all__'
        extra_kwargs = {
         
            # 'cutomer': {'cutomer': True},
            # 'shopkeeper':{'required': True},
            'total_amount': {'required': True},
             'discount': {'required': True},
           

        }




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

class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=128, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        read_only_fields=['token']

class GiftSpineSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftSpin
        fields = ['name', 'quantity', 'amount']

class SpineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spines
        fields = ['spine_no', 'shopkeeper', 'order']


#
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         token['id'] = user.id
#         token['user_type'] = user.user_type
#         data =token
#
#         print('hwllo', token['user_type'])
#         return data