import re

from numpy import product
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from shopkeeper.models.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, \
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status

def check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # to validate emails only
    if (re.fullmatch(regex, email)):

        return True
    else:

        return False



class EmployeeViewSetApi(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # def list(self, request):
    #     print('list Employee')
    #     employees = Employee.objects.all()
    #     serializer = EmployeeSerializer(employees, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
                employee = Employee.objects.get(id=pk)
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
        post_data = request.data
        employee = Employee.objects.get(id=id)
        user = User.objects.get(id=employee.user.id)
        user.username = post_data['user']['username']
        user.first_name = post_data['user']['first_name']
        user.last_name = post_data['user']['last_name']
        user.email = post_data['user']['email']
        user.address = post_data['user']['address']
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
        post_data=request.data

        user_data = post_data.get('user', None)
        if user_data:
            employee = Employee.objects.get(id=pk)
            user = User.objects.get(id=employee.user.id)
            user.username = user_data.get('username', user.username)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.address = user_data.get('address', user.address)
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

    # def list(self, request):
    #
    #     dukandar = Shopkeeper.objects.all()
    #     serializer = ShopkeeperSerializer(dukandar, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        try:
            dukandar = Shopkeeper.objects.get(id=pk)
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
            username = post_data['username']
            email = post_data['email']
            user_exist = User.objects.filter(username=username)
            if user_exist:
                response = {
                    'Error': 'Same User Name is already Existed ' + username
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
                copyied_dict = post_data.copy()
                print('emp_exitsss')
                employee_obj= Employee.objects.get(id=employ_id)
                print('emp_exit',employee_obj)
                if employee_obj:
                    user = User.objects.create(username=post_data['username'], password=post_data['password'],
                                               email=post_data['email'], first_name=post_data['first_name'],
                                               last_name='last_name',
                                               address=post_data['address'])
                    user.user_type = 'SHOPKEEPER'
                    user.save()
                    employee = Employee.objects.get(id=post_data['emp_id'])
                    dukandar = Shopkeeper.objects.create(user=user, shop_name=post_data['shop_name'],
                                                         phone_no=post_data['phone_no'], latitude=post_data['latitude'],
                                                         longitude=post_data['longitude'], emp_id=employee_obj)
                    dukandar.save()
            except Employee.DoesNotExist:
                response = {
                    'message': 'Employee Does Not Exist'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer = ShopkeeperSerializer(data=post_data)
            print(serializer)

            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            response = {
                'message': 'User Already Exist'
             }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)



    def update(self, request, pk):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        post_data = request.data
        dukandar = Shopkeeper.objects.get(id=pk)
        user = User.objects.get(id=dukandar.user.id)
        user.username = post_data['user']['username']
        user.first_name = post_data['user']['first_name']
        user.last_name = post_data['user']['last_name']
        user.email = post_data['user']['email']
        user.address = post_data['user']['address']
        user.user_type = 'SHOPKEEPER'
        user.save()

        serializer = ShopkeeperSerializer(dukandar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        post_data = request.data
        dukandar = Shopkeeper.objects.get(id=pk)

        user_data = post_data.get('user',None)
        if user_data:
            dukandar = Shopkeeper.objects.get(id=pk)
            user = User.objects.get(id=dukandar.user.id)
            user.username = user_data.get('username', user.username)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.address = user_data.get('address', user.address)
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
        dukandar = Shopkeeper.objects.get(id=pk)
        dukandar.delete()
        response = {
            'message': 'Record Deleted Successfully'
        }
        return Response(response, status=status.HTTP_200_OK)


class CustomerViewSetApi(viewsets.ViewSet):

    def list(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        post_data = request.data
        username = post_data['username']
        email = post_data['email']
        user_exist = User.objects.filter(username=username)
        if user_exist:
            response = {
                'Error': 'Same User Name is already Existed ' + username
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
        user = User.objects.create_user(username=post_data['username'], password=post_data['password'],
                                        email=post_data['email'], first_name=post_data['first_name'],
                                        last_name='last_name',
                                        address=post_data['address'])
        user.user_type = 'CUSTOMER'
        user.save()
        customer = Customer.objects.create(phone_no=post_data['phone_no'], user=user)
        customer.save()
        print('customer', customer)
        serializer = CustomerSerializer(data=customer)
        print('serializerCustomer', serializer)
        if serializer.is_valid():
            print('save ser')
            serializer.save()
            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            print('serialize.errors',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            customer = Customer.objects.get(id=pk)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            response = {
                'message': 'No Record Found'
            }
            return Response(response, status=status.HTTP_200_OK)

    def update(self, request, pk):
        post_data = request.data
        id = pk
        customer = Customer.objects.get(id=id)
        user = User.objects.get(id=customer.user.id)
        user.username = post_data['user']['username']
        user.first_name = post_data['user']['first_name']
        user.last_name = post_data['user']['last_name']
        user.email = post_data['user']['email']
        user.address = post_data['user']['address']
        user.user_type = 'CUSTOMER'
        user.save()
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        post_data = request.data
        user_data = post_data['user']
        customer = Customer.objects.get(id=pk)
        user = User.objects.get(id=customer.user.id)
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.address = user_data.get('address', user.address)
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

    def destroy(self, request, pk):
        customer = Customer.objects.get(id=pk)
        customer.delete()
        response = {
            'message': 'Record Deleted Successfully'
        }
        return Response(response, status=status.HTTP_200_OK)


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



class userRegistration(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()
        # user = request.user
        # if user is not None:
        #     users = User.objects.filter(email=user)
        # else:
        #     users = User.objects.all()
        print('user is>> ', users)
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        print('hello', request.data)

        serializer = UserRegistrationSerializer(data=request.POST)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Record Created successfully.'
            data['email'] = user.email
            data['username'] = user.username
            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            user = User.objects.get(id=id)
            serializer = UserRegistrationSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        print("********List*******")
        print("BaseName:>>", self.basename)
        print("action:>>", self.action)
        print("detail:>>", self.detail)
        print("suffix:>>", self.suffix)
        print("description:>>", self.description)
        print("description:>>", self.description)
        id = pk
        user = User.objects.get(id=id)
        serializer = UserRegistrationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        id = pk
        user = User.objects.get(id=id)
        serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Partial Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


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
            post_data=request.data

            customer_id =post_data.get('customer', None)
            shopkeeper_id =post_data.get('shopkeeper', None)

            if customer_id:
                try:
                    customer_obj=Customer.objects.get(id=customer_id)
                    if customer_obj:
                        serializer = OrderSerializer(data=post_data)

                        if serializer.is_valid():

                            serializer.save()
                            print('serializer',serializer)
                            response = {
                            'message': 'Order Created Successfully'
                                }
                            return Response(response, status=status.HTTP_201_CREATED)
                except  Customer.DoesNotExist:
                    response = {
                        'message': 'Customer with Id Does Not Exist For this Order'
                            }
                    return Response(response,status=status.HTTP_400_BAD_REQUEST)

            else:

                try:
                    shopkeeper_obj=Shopkeeper.objects.get(id=shopkeeper_id)
                    if shopkeeper_obj:
                        serializer = OrderSerializer(data=post_data)

                        if serializer.is_valid():
                            order =serializer.save()
                            amount=float(post_data['amount'])
                            if amount > float(100000) and amount < float(250000):
                                wallet =Wallet.objects.create(shopkeeper=shopkeeper_obj,order=order,amount=1000)
                                wallet.save()

                            if amount > float(250000) and amount < float(500000):
                                wallet =Wallet.objects.create(shopkeeper=shopkeeper_obj,order=order,amount=2500)
                                wallet.save()
                            if amount > float(500000):
                                wallet =Wallet.objects.create(shopkeeper=shopkeeper_obj,order=order,amount=7500)
                                wallet.save()
                            if amount > float(250000) and amount < float(500000):
                                spine =Spines.objects.create(shopkeeper=shopkeeper_obj,order=order,amount=1)
                                spine.save()
                            if amount > float(500000) and amount < float(1000000):
                                spine =Spines.objects.create(shopkeeper=shopkeeper_obj,order=order,amount=2)
                                spine.save()
                            response = {
                            'message': 'Order Created Successfully',
                            'order_id':order.id

                                }
                            return Response(response, status=status.HTTP_201_CREATED)

                except  Shopkeeper.DoesNotExist:

                    response = {
                        'message': 'Shopkeeper with Id Does Not Exist For this Order'
                            }
                    return Response(response,status=status.HTTP_400_BAD_REQUEST)
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