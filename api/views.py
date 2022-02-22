import re
from copy import deepcopy

from numpy import product
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from shopkeeper.models.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, \
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
import jwt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status


def tokenCheck(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated Error!  Please Login first to move ahead')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated Error!  Please Login first to move ahead')


def check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # to validate emails only
    if (re.fullmatch(regex, email)):

        return True
    else:

        return False


class EmployeeViewSetApi(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        tokenCheck(request)
        print('list Employee')

        # employees = Employee.objects.all()
        # serializer = EmployeeSerializer(employees, many=True)
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        tokenCheck(request)
        try:
            user = User.objects.get(id=pk)
            employee = Employee.objects.get(user=user)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            response = {
                'message': 'Record Not Found'
            }
            return Response(response, status=status.HTTP_200_OK)

    # def create(self, request):
    #     print('create Employee', request.POST)
    #     serializer = EmployeeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #             'message': 'Record Created Successfully !'
    #         }
    #         return Response(response, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        tokenCheck(request)
        post_data = request.data
        user = User.objects.get(id=pk)
        employee = Employee.objects.get(user=user)
        user.first_name = post_data['first_name']
        user.last_name = post_data['last_name']
        user.email = post_data['email']
        user.address = post_data['address']
        user.city = post_data['city']
        user.phone_no = post_data['phone_no']
        user.user_type = 'SHOPKEEPER'
        user.save()
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        tokenCheck(request)
        post_data = request.data
        user = User.objects.get(id=pk)
        employee = Employee.objects.get(user=user)
        user.first_name = post_data.get('first_name', user.first_name)
        user.last_name = post_data.get('last_name', user.last_name)
        user.email = post_data.get('email', user.email)
        user.address = post_data.get('address', user.address)
        user.city = post_data.get('city', user.username)
        user.phone_no = post_data.get('phone_no', user.username)
        user.user_type = 'STAFF'
        user.save()

        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Partial Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk):
    #     employee = Employee.objects.get(id=pk)
    #     employee.delete()
    #     response = {
    #         'message': 'Record Deleted Successfully'
    #     }
    #     return Response(response, status=status.HTTP_200_OK)


class ShopkeeperViewSetApi(viewsets.ViewSet):

    def list(self, request):

        dukandar = Shopkeeper.objects.all()
        serializer = ShopkeeperSerializer(dukandar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        # authentication_classes = [JWTAuthentication]
        # permission_classes = [IsAuthenticated]
        tokenCheck(request)
        try:
            user = User.objects.get(id=pk)
            dukandar = Shopkeeper.objects.get(user=user)
            serializer = ShopkeeperSerializer(dukandar)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Shopkeeper.DoesNotExist:
            response = {
                'Message': 'No Record Found'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            post_data = request.data
            email = post_data['email']
            user_exist = User.objects.filter(email=email)
            if user_exist:
                response = {
                    'Message': 'Email is Already Existed'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            validate_email = check(email)
            if not validate_email:
                response = {
                    'Error': 'Email is not in Proper Format ' + email
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password != password2:
                response = {
                    'Error': 'Password Must be Same !'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            try:
                employ_id = post_data.get('emp_id', None)
                emp_user =User.objects.get(email=employ_id)
                employee_obj=Employee.objects.get(user=emp_user)



                if employee_obj:
                    user = User.objects.create_user(email=post_data['email'],password=post_data['password'])
                    user.first_name=post_data['first_name'],
                    user.last_name = post_data['last_name'],
                    user.address=post_data['address']
                    user.city = post_data['city'],
                    user.phone_no = post_data['phone_no']
                    user.user_type = 'SHOPKEEPER'
                    user.save()
                    dukandar = Shopkeeper.objects.create(user=user, shop_name=post_data['shop_name'],
                                                        latitude=post_data['latitude'],
                                                         longitude=post_data['longitude'], emp_id=employee_obj)
                    dukandar.save()
            except Employee.DoesNotExist:
                response = {
                    'message': 'Employee with this Email Does Not Exist'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer = ShopkeeperSerializer(data=post_data)
            print(serializer)

            response = {
                'message': 'Record ddCreated Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)

        except:
            serializer = ShopkeeperSerializer(data=request.data)
            if serializer.is_valid():
                response = {
                    'message': 'Something Went Wrong'
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        tokenCheck(request)
        post_data = request.data
        dukandar = Shopkeeper.objects.get(user=pk)
        user = User.objects.get(id=dukandar.user.id)

        user.email = post_data['email']
        user.first_name = post_data['first_name']
        user.last_name = post_data['last_name']
        user.city = post_data['city']
        user.address = post_data['address']
        user.phone_no = post_data['phone_no']
        user.user_type = 'SHOPKEEPER'
        user.save()


        user_obj =User.objects.get(email=post_data['emp_id'])
        employee =Employee.objects.get(user=user_obj)
        dukandar.emp_id=employee
        dukandar.save()
        serializer = ShopkeeperSerializer(dukandar,data=post_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        tokenCheck(request)
        post_data = request.data

        dukandar = Shopkeeper.objects.get(user=pk)
        user = User.objects.get(id=dukandar.user.id)
        user.email = post_data.get('email', user.email)

        user.first_name = post_data.get('first_name', user.first_name)
        user.last_name = post_data.get('last_name', user.last_name)
        user.address = post_data.get('address', user.address)
        user.city = post_data.get('city', user.city)
        user.phone_no = post_data.get('phone_no', user.phone_no)
        user.user_type = 'SHOPKEEPER'
        user.save()
        serializer = ShopkeeperSerializer(dukandar, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Partial Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        tokenCheck(request)
        dukandar = Shopkeeper.objects.get(id=pk)
        dukandar.delete()
        response = {
            'message': 'Record Deleted Successfully'
        }
        return Response(response, status=status.HTTP_200_OK)


class CustomerViewSetApi(viewsets.ViewSet):

    # def list(self, request):
    #     customers = Customer.objects.all()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        post_data = request.data
        email = post_data.get('email')
        validate_email = None
        if email:
            validate_email = check(email)
        if validate_email:
            user_exist = User.objects.filter(email=email)
            if user_exist:
                response = {
                    'Error': 'Email is already Existed ' + email
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                password = request.POST.get('password')
                password2 = request.POST.get('password2')
                if password != password2:
                    response = {
                        'Error': 'Password and password2 Must be Same !'
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.create_user(email=post_data['email'], password=post_data['password'])
                user.first_name = post_data['first_name']
                user.last_name = post_data['last_name']
                user.phone_no = post_data['phone_no']
                user.city = post_data['city']
                user.address = post_data['address']
                user.user_type = 'CUSTOMER'
                user.save()
                customer = Customer.objects.create(user=user)
                customer.save()
                response = {
                    'message': 'Customer Created Successfully'
                }
                return Response(response, status=status.HTTP_200_OK)



        else:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                response = {
                    'message': 'Record Created Successfully !'
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        tokenCheck(request)
        try:
            user =User.objects.get(id=pk)
            customer = Customer.objects.get(user=user)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            response = {
                'message': 'No Record Found'
            }
            return Response(response, status=status.HTTP_200_OK)

    def update(self, request, pk):
        tokenCheck(request)

        post_data = request.data
        print('post_data Update', post_data)
        id = pk
        customer = Customer.objects.get(id=id)
        user = User.objects.get(id=customer.user.id)
        # user.email = post_data['email']
        user.first_name = post_data['first_name']
        user.last_name = post_data['last_name']
        user.phone_no = post_data['phone_no']
        user.city = post_data['city']
        user.address = post_data['address']
        user.user_type = 'CUSTOMER'
        user.save()
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'message': 'Something went wrong'
        }
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        tokenCheck(request)
        post_data = request.data
        customer = Customer.objects.get(id=pk)
        user = User.objects.get(id=customer.user.id)
        user.first_name = post_data.get('first_name', user.first_name)
        user.last_name = post_data.get('last_name', user.last_name)
        user.email = post_data.get('email', user.email)
        user.phone_no = post_data.get('phone_no', user.phone_no)
        user.city = post_data.get('city', user.city)
        user.address = post_data.get('address', user.address)
        user.user_type = 'CUSTOMER'
        user.save()
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Partial Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk):
    #     customer = Customer.objects.get(id=pk)
    #     customer.delete()
    #     response = {
    #         'message': 'Record Deleted Successfully'
    #     }
    #     return Response(response, status=status.HTTP_200_OK)


class ProductViewSetApi(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:

            response = {
                'message': 'No Product Found'
            }

            return Response(response, status=status.HTTP_200_OK)

    # def create(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #             'message': 'Record Created Successfully !'
    #         }
    #         return Response(response, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, pk):

    #     id = pk
    #     product = Product.objects.get(id=id)
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #             'message': 'Complete Record Update Successfully'
    #         }
    #         return Response(response, status=status.HTTP_200_OK)
    #     return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, pk):
    #     id = pk
    #     product = Product.objects.get(id=id)
    #     serializer = ProductSerializer(product, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #             'message': 'Partial Record Update Successfully'
    #         }
    #         return Response(response, status=status.HTTP_200_OK)
    #     return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk):
    #     product = Product.objects.get(id=pk)
    #     product.delete()
    #     response = {
    #         'message': 'Record Deleted Successfully'
    #     }
    #     return Response(response, status=status.HTTP_200_OK)


class ParentCategoryView(viewsets.ViewSet):
    def list(self, request):
        tokenCheck(request)
        parents = ParentCategory.objects.filter(is_active=True)
        serializer = ParentCategorySerializer(parents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        tokenCheck(request)
        try:

            parent = ParentCategory.objects.get(id=pk)
            sub_cate = SubCategory.objects.filter(parent=parent.id, is_active=True)
            serializer = SubCategorySerializer(sub_cate, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ParentCategory.DoesNotExist:

            response = {
                'message': 'No Parent Category  Found'
            }

            return Response(response, status=status.HTTP_200_OK)


class SubCategoryView(viewsets.ViewSet):
    # def list(self, request):
    #     sub_cat = SubCategory.objects.all()
    #     serializer = ParentCategorySerializer(sub_cat, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        tokenCheck(request)
        try:
            parent = SubCategory.objects.get(id=pk)
            products_list = Product.objects.filter(parent=parent.id, is_active=True)
            serializer = ProductSerializer(products_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ParentCategory.DoesNotExist:

            response = {
                'message': 'No Parent Category  Found'
            }

            return Response(response, status=status.HTTP_200_OK)


class OrderViewSetApi(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # def list(self, request):
    #     orders = Order.objects.all()
    #     serializer = OrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(id=id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            response = {
                'message': 'No Order Found'
            }
            return Response(response, status=status.HTTP_200_OK)

    def create(self, request):

        try:
            post_data = request.data

            customer_id = post_data.get('customer', None)
            shopkeeper_id = post_data.get('shopkeeper', None)

            if customer_id:
                try:
                    customer_obj = Customer.objects.get(id=customer_id)
                    if customer_obj:
                        serializer = OrderSerializer(data=post_data)

                        if serializer.is_valid():
                            serializer.save()
                            print('serializer', serializer)
                            response = {
                                'message': 'Order Created Successfully'
                            }
                            return Response(response, status=status.HTTP_201_CREATED)
                except  Customer.DoesNotExist:
                    response = {
                        'message': 'Customer with Id Does Not Exist For this Order'
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

            else:

                try:
                    shopkeeper_obj = Shopkeeper.objects.get(id=shopkeeper_id)
                    if shopkeeper_obj:
                        serializer = OrderSerializer(data=post_data)

                        if serializer.is_valid():
                            order =serializer.save()
                            amount=float(post_data['amount'])

                            if amount < float(100000):
                                wallet =Wallet.objects.create(shopkeeper=shopkeeper_obj,order=order,amount=0)
                                wallet.save()

                            if amount > float(100000) and amount < float(250000):
                                wallet = Wallet.objects.create(shopkeeper=shopkeeper_obj, order=order, amount=1000)
                                wallet.save()

                            if amount > float(250000) and amount < float(500000):
                                wallet = Wallet.objects.create(shopkeeper=shopkeeper_obj, order=order, amount=2500)
                                wallet.save()
                                spine =Spines.objects.create(shopkeeper=shopkeeper_obj,order=order,amount=1)
                                spine.save()
        
                            if amount > float(500000):
                                wallet = Wallet.objects.create(shopkeeper=shopkeeper_obj, order=order, amount=7500)
                                wallet.save()
                                spine =Spines.objects.create(shopkeeper=shopkeeper_obj,order=order,amount=2)
                                spine.save()
                           
                            response = {
                                'message': 'Order Created Successfully',
                                'order_id': order.id

                            }
                            return Response(response, status=status.HTTP_201_CREATED)

                except  Shopkeeper.DoesNotExist:

                    response = {
                        'message': 'Shopkeeper with Id Does Not Exist For this Order'
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:

            response = {
                'message': 'Please Provide Orders Parmeter'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, pk):
    #     print("********List*******")
    #     print("BaseName:>>", self.basename)
    #     print("action:>>", self.action)
    #     print("detail:>>", self.detail)
    #     print("suffix:>>", self.suffix)
    #     print("description:>>", self.description)
    #     print("description:>>", self.description)
    #     id = pk
    #     order = Order.objects.get(id=id)
    #     serializer = OrderSerializer(order, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #             'message': 'Complete Record Update Successfully'
    #         }
    #         return Response(response, status=status.HTTP_200_OK)
    #     return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    #
    # def partial_update(self, request, pk):
    #     id = pk
    #     order = Order.objects.get(id=id)
    #     serializer = OrderSerializer(order, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #             'message': 'Partial Record Update Successfully'
    #         }
    #         return Response(response, status=status.HTTP_200_OK)
    #     return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk):
    #     order = Order.objects.get(id=pk)
    #     order.delete()
    #     response = {
    #         'message': 'Record Deleted Successfully'
    #     }
    #     return Response(response, status=status.HTTP_200_OK)


class SpinesViewSetApi(viewsets.ViewSet):
    def list(self, request):
        spines = Spines.objects.all()
        serializer = OrderSerializer(spines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalletViewSetApi(viewsets.ViewSet):
    def list(self, request):
        wallet = Wallet.objects.all()
        serializer = OrderSerializer(wallet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GiftSpineViewSetApi(viewsets.ViewSet):

    def list(self, request):
        tokenCheck(request)
        gifts = GiftSpin.objects.all()
        serializer = GiftSpineSerializer(gifts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        print('rew', request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        print('user', user)
        if user:
            serializer = self.serializer_class(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message:" Invalid Credentail"'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            user = User.objects.filter(email=email).first()
            if user is None:
                raise AuthenticationFailed('User Not Found')
            if not user.check_password(password):
                raise AuthenticationFailed('Incorrect password!')
            payload = {
                'id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                # 'user_type':user.user_type,
            }
            token = token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=15)},
                                       settings.SECRET_KEY, algorithm='HS256')
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'jwt': token,
                'user_id': user.id,
                'user_type': user.user_type
            }
            return response
        return Response({'message:" Please Enter Email & Password"'}, status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id'])
        serializers = CustomerSerializer(user)
        return Response(serializers.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successfully logout'
        }
        return response
