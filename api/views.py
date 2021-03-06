import re
from copy import deepcopy
import json
from urllib import request
from numpy import product
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, generics
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
            employe_data = serializer.save()
            emp_histroy = EmployeeHistry.objects.create(employee=employe_data,
                                                        daily_target_assign=employe_data.target_assign,
                                                        daily_achieved=employe_data.target_achieved)
            emp_histroy.save()
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
            employe_data = serializer.save()
            emp_histroy = EmployeeHistry.objects.create(employee=employe_data,
                                                        daily_target_assign=employe_data.target_assign,
                                                        daily_achieved=employe_data.target_achieved)
            emp_histroy.save()
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

    #     dukandar = Shopkeeper.objects.all()
    #     serializer = ShopkeeperSerializer(dukandar, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        # authentication_classes = [JWTAuthentication]
        # permission_classes = [IsAuthenticated]
        tokenCheck(request)
        try:
            user = User.objects.get(id=pk)

            dukandar = Shopkeeper.objects.get(user=user)

            total_orders = Order.objects.filter(shopkeeper=dukandar.id).count()
            walt_obj = Wallet.objects.filter(shopkeeper=dukandar.id)
            walt_amount = 0
            if walt_obj:
                walt_amount = walt_obj[0].amount
            spin_obj = Spines.objects.filter(shopkeeper=dukandar.id)
            total_spin = 0
            if spin_obj:
                total_spin = spin_obj[0].spine_no
            serializer = ShopkeeperSerializer(dukandar)
            context = {
                'shopkeeper': serializer.data,
                'spin': total_spin,
                'wallet': walt_amount,
                'orders': total_orders,
                'shopkeeper_type': dukandar.shopkeeper_type
            }
            return Response(context, status=status.HTTP_200_OK)
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
                employee_obj = None
                if employ_id:
                    emp_user = User.objects.get(email=employ_id)

                    employee_obj = Employee.objects.get(user_id=emp_user.id)

                    employee_obj.target_achieved += 1
                    employee_obj.save()
                    emp_histroy = EmployeeHistry.objects.create(employee=employee_obj,
                                                                daily_target_assign=employee_obj.target_assign,
                                                                daily_achieved=employee_obj.target_achieved)
                    emp_histroy.save()
                user = User.objects.create_user(email=post_data['email'], password=post_data['password'])
                user.first_name = post_data['first_name'],
                user.last_name = post_data['last_name'],
                user.address = post_data['address']
                user.city = post_data['city'],
                user.phone_no = post_data['phone_no']
                user.user_type = 'SHOPKEEPER'
                user.save()
                dukandar = Shopkeeper.objects.create(user=user, shop_name=post_data['shop_name'],
                                                     latitude=post_data['latitude'],
                                                     longitude=post_data['longitude'],
                                                     shopkeeper_type=post_data['shopkeeper_type'],
                                                     emp_id=employee_obj)

                dukandar.save()
            except Employee.DoesNotExist:
                response = {
                    'message': 'Employee with this Email Does Not Exist'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer = ShopkeeperSerializer(data=post_data)
            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)

        except:
            serializer = ShopkeeperSerializer(data=request.data)
            if serializer.is_valid():
                response = {
                    'message': 'Record Created Successfully !'
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        tokenCheck(request)
        post_data = request.data
        dukandar = Shopkeeper.objects.get(user=pk)
        user = User.objects.get(id=pk)

        user.email = post_data['email']
        user.first_name = post_data['first_name']
        user.last_name = post_data['last_name']
        user.city = post_data['city']
        user.address = post_data['address']
        user.phone_no = post_data['phone_no']
        user.user_type = 'SHOPKEEPER'
        user.save()

        # user_obj = User.objects.get(email=post_data['emp_id'])
        # employee = Employee.objects.get(user=user_obj)
        # dukandar.emp_id = employee
        employee = Employee.objects.get(user__email=post_data['emp_id'])
        dukandar.emp_id = employee
        dukandar.save()
 
        serializer = ShopkeeperSerializer(dukandar, data=post_data)
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
        # user_obj = User.objects.get(email=post_data['emp_id'])

        emp_id=post_data.get('emp_id', None)
        if emp_id:
            employee = Employee.objects.get(user__email=emp_id)
            dukandar.emp_id = employee or dukandar.emp_id
            dukandar.save()
        
        serializer = ShopkeeperSerializer(dukandar, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Partial Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk):
    #     tokenCheck(request)
    #     dukandar = Shopkeeper.objects.get(id=pk)
    #     dukandar.delete()
    #     response = {
    #         'message': 'Record Deleted Successfully'
    #     }
    #     return Response(response, status=status.HTTP_200_OK)


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
            user = User.objects.get(id=pk)
            customer = Customer.objects.get(user=user)
            serializer = CustomerSerializer(customer)
            context = {
                'customer': serializer.data,

                'orders': Order.objects.filter(customer=customer.id).count()
            }
            return Response(context, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            response = {
                'message': 'No Record Found'
            }
            return Response(response, status=status.HTTP_200_OK)

    def update(self, request, pk):
        tokenCheck(request)

        post_data = request.data
        customer = Customer.objects.get(user=pk)
        user = User.objects.get(id=pk)
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
        customer = Customer.objects.get(user=pk)
        
        user = User.objects.get(id=pk)
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


class AllProductApi(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllProductApi(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductViewSetApi(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        tokenCheck(request)
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        try:
            tokenCheck(request)
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
        print('pk', pk)
        # tokenCheck(request)
        try:
            parent = SubCategory.objects.get(id=pk)
            print('parent',parent)
            products_list = Product.objects.filter(sub_cat=parent.id, is_active=True, quantity__gt=0)
            print('products_list',products_list)
            serializer = ProductSerializer(products_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ParentCategory.DoesNotExist:

            response = {
                'message': 'No Parent Category  Found'
            }

            return Response(response, status=status.HTTP_200_OK)


class OrderViewSetApi(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    # def list(self, request):
    #     orders = Order.objects.all()
    #     serializer = OrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        tokenCheck(request)
        try:
            orderItm_LIST =[]
            shopkeeper = Shopkeeper.objects.get(user_id=pk)

            order_obj = Order.objects.filter(shopkeeper_id=shopkeeper.id)
            orderItm_List =[]
            for ord in order_obj:
                order_item =ProductOrder.objects.filter(order=ord)
                test_dict =[]
                for item in order_item:
                    test_dict.append({
                            'product':item.product.name,
                            'quantity':item.quantity,
                            'price':item.price,
                            'sub_total':item.sub_total
                    })
                   
                 
                orderItm_LIST.append({
                    
                    'order#':ord.id,
                    'status':ord.status,
                    'order_date':ord.created_at,
                    'last_updated': ord.updated_at,
                    'orderItem':test_dict
                    })
            orderItm_List.append({
                    'user':pk,
                    'orders':orderItm_LIST
            })
            # order_itm =ProductOrder.objects.all()
            # serializer = OrderSerializer(order_obj, many=True)

            # serializer1 = ProductOrderSerializer(order_obj, many=True)
            # data_dict ={
            #     'order':serializer.data,
            #      'orderItem':serializer1.data
            # }

            # print('serializer1',serializer1.data)
            return Response(orderItm_List, status=status.HTTP_200_OK)

        except Shopkeeper.DoesNotExist:
            try:
                
                orderItm_LIST = []
                customer = Customer.objects.get(user_id=pk)

                order_obj = Order.objects.filter(customer_id=customer.id)
                orderItm_List = []
                for ord in order_obj:
                    order_item = ProductOrder.objects.filter(order=ord)
                    test_dict = []
                    for item in order_item:
                        test_dict.append({
                            'product': item.product.name,
                            'quantity': item.quantity,
                            'price': item.price,
                            'sub_total': item.sub_total
                        })

                    orderItm_LIST.append({

                        'order#': ord.id,
                        'status': ord.status,
                        'order_date': ord.created_at,
                        'last_updated':ord.updated_at,
                        'orderItem': test_dict
                    })
                orderItm_List.append({
                    'user': pk,
                    'orders': orderItm_LIST
                })
                return Response(orderItm_List, status=status.HTTP_200_OK)
            except Customer.DoesNotExist:
                response = {
                    'message': 'No Order Found'
                }
                return Response(response, status=status.HTTP_200_OK)

    def create(self, request):
        tokenCheck(request)
        try:
            post_data = request.data

            post_Data = deepcopy(post_data)
            products = post_Data.get('products', None)
            customer_id = post_data.get('customer', None)
            shopkeeper_id = post_data.get('shopkeeper', None)

            if customer_id:
                try:

                    user = User.objects.get(id=customer_id)
                    print('user',user)
                    customer_obj = Customer.objects.get(user=customer_id)

                    if customer_obj:
                        post_Data['customer'] = customer_obj.id
                        serializer = OrderSerializer(data=post_Data)
                        if serializer.is_valid():
                            serializer.save()
                            order = serializer.save()
                            ord_history = OrderHistory.objects.create(order=order)
                            ord_history.save()

                            for index in range(len(products)):
                                product_id = products[index]['id']
                                qty = products[index]['quantity']
                                price = products[index]['amount']
                                sub_total = products[index]['subtotal']
                                order_prod = ProductOrder.objects.create(order_id=order.id, product_id=product_id,
                                                                         quantity=qty, sub_total=sub_total, price=price)

                                order_prod.save()
                                order_prod_hist = ProductOrderHistory.objects.create(order=ord_history,
                                                                                     product_id=product_id,
                                                                                     quantity=qty, sub_total=sub_total,
                                                                                     price=price)
                                order_prod_hist.save()
                                product_objs = Product.objects.get(id=product_id)
                                qty = product_objs.quantity - qty
                                if qty < 0:
                                    product_objs.quantity = 0
                                else:
                                    product_objs.quantity = qty
                                product_objs.save()

                            response = {
                                'message': 'Order Created Successfully'
                            }
                            return Response(response, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except  Customer.DoesNotExist:
                    response = {
                        'message': 'Customer with Id Does Not Exist For this Order'
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

            else:

                try:

                    users = User.objects.get(id=shopkeeper_id)
                    shopkeeper_obj = Shopkeeper.objects.get(user=shopkeeper_id)
                    if shopkeeper_obj:

                        post_Data['shopkeeper'] = shopkeeper_obj.id

                        serializer = OrderSerializer(data=post_Data)
                        if serializer.is_valid():
                            order = serializer.save()
                            ord_history = OrderHistory.objects.create(order=order)
                            ord_history.save()
                            # ord_history = OrderHistory.objects.create(shopkeeper=shopkeeper_obj,
                            #                                           total_amount=post_Data['total_amount'],
                            #                                           discount=post_Data['discount'])
                            ord_history.save()
                            for index in range(len(products)):

                                product_id = products[index]['id']
                                qty = products[index]['quantity']
                                price = products[index]['amount']
                                sub_total = products[index]['subtotal']
                              
                                order_prod = ProductOrder.objects.create(order_id=order.id, product_id=product_id,
                                                                         quantity=qty, sub_total=sub_total, price=price)

                                order_prod.save()

                                order_prod_hist = ProductOrderHistory.objects.create(order_id=ord_history.id,
                                                                                     product_id=product_id,
                                                                                     quantity=qty, sub_total=sub_total,
                                                                                     price=price)
                               
                                order_prod_hist.save()

                                product_objs = Product.objects.get(id=product_id)
                                qty = product_objs.quantity - qty
                                product_objs.quantity = qty
                                quantiy_hist = product_objs.quantity
                                product_objs.save()

                                order_prod_hist = ProductOrderHistory.objects.create(order_id=ord_history.id,
                                                                                     product_id=product_id,
                                                                                     quantity=quantiy_hist,
                                                                                     sub_total=sub_total,
                                                                                     price=price)
                                order_prod_hist.save()

                            total_amount = float(post_data['total_amount'])
                            if total_amount < float(100000):
                                try:
                                    wallet_obj = Wallet.objects.get(shopkeeper_id=shopkeeper_obj.id)
                                    wallet_obj.order = order
                                    wallet_obj.amount = 0
                                    wallet_obj.save()

                                except:
                                    wallet = Wallet.objects.create(shopkeeper=shopkeeper_obj, order=order, amount=0)
                                    wallet.save()

                            if total_amount > float(100000) and total_amount < float(250000):
                                try:
                                    wallet_obj = Wallet.objects.get(shopkeeper_id=shopkeeper_obj.id)
                                    wallet_obj.order = order
                                    wallet_obj.amount = 1000
                                    wallet_obj.save()

                                except:
                                    wallet = Wallet.objects.create(shopkeeper=shopkeeper_obj, order=order, amount=1000)
                                    wallet.save()

                            if total_amount > float(250000) and total_amount < float(500000):
                                try:
                                    wallet_obj = Wallet.objects.get(shopkeeper_id=shopkeeper_obj.id)
                                    wallet_obj.order = order
                                    wallet_obj.amount = 2500
                                    wallet_obj.save()
                                    spine = Spines.objects.get(shopkeeper_id=shopkeeper_obj.id)
                                    spine.spine_no +=1
                                    spine.save()

                                except:
                                    wallet = Wallet.objects.create(shopkeeper=shopkeeper_obj, order=order, amount=2500)
                                    wallet.save()
                                    spine = Spines.objects.create(shopkeeper=shopkeeper_obj, order=order, spine_no=1)
                                    spine.save()

                            if total_amount > float(500000):
                                try:
                                    wallet_obj = Wallet.objects.get(shopkeeper_id=shopkeeper_obj.id)
                                    wallet_obj.order = order
                                    wallet_obj.amount = 7500
                                    wallet_obj.save()
                                    spine = Spines.objects.get(shopkeeper_id=shopkeeper_obj.id)
                                    spine.spine_no +=2
                                    spine.save()

                                except:
                                    wallet = Wallet.objects.create(shopkeeper=shopkeeper_obj, order=order, amount=7500)
                                    wallet.save()
                                    spine = Spines.objects.create(shopkeeper=shopkeeper_obj, order=order, spine_no=2)
                                    spine.save()

                            response = {
                                'message': 'Order Created Successfully',
                                'order_id': order.id

                            }
                            return Response(response, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
   
    # def partial_update(self, request, pk):
    #     # tokenCheck(request)
    #     post_data = request.data
    #     print('request.data', request.data, 'PK', pk)
    #     try:
    #         order = Order.objects.get(id=pk)
    #         # user = User.objects.get(id=customer.user.id)
      
    #         if post_data.get('status') =='CANCELLED':
    #             order.status = post_data.get('status', order.status)    
    #             order.save()
    #             serializer = OrderSerializer(order, data=request.data, partial=True)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 response = {
    #                     'message': 'Partial Record Update Successfully'
    #                 }
    #                 return Response(response, status=status.HTTP_200_OK)
    #             return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             response = {
    #                 'message': 'You can only Cancelled your Order'
    #             }
    #             return Response(response, status=status.HTTP_400_BAD_REQUEST)
    #     except Order.DoesNotExist:  
    #          response = {
    #                 'message': 'Order Does Not Updated'
    #             }
    #          return Response(response, status=status.HTTP_400_BAD_REQUEST)
class SpinesViewSetApi(viewsets.ViewSet):

    def list(self, request):
        tokenCheck(request)
        spines = Spines.objects.all()
        serializer = SpineSerializer(spines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalletViewSetApi(viewsets.ViewSet):

    def list(self, request):
        tokenCheck(request)
        wallet = Wallet.objects.all()
        serializer = OrderSerializer(wallet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        tokenCheck(request)
        try:
            post_data = request.data
            shopkeeperId = post_data.get('shopkeeperId', None)
            users = User.objects.get(id=shopkeeperId)
            shopkeeper_obj = Shopkeeper.objects.get(user=shopkeeperId)
            wallet_obj = Wallet.objects.get(shopkeeper_id=shopkeeper_obj.id)
            wallet_obj.amount = post_data.get('amount', wallet_obj.amount)
            wallet_obj.save()
    
            response = {
                'message': 'Gift Amount Added Successfully'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except:
            response = {
                'message': 'Gift Amount not added '
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GiftSpineViewSetApi(viewsets.ViewSet):

    def list(self, request):
        tokenCheck(request)
        gifts = GiftSpin.objects.filter(quantity__gt=0)
        serializer = GiftSpineSerializer(gifts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        tokenCheck(request)
        post_data = request.data
        post_Data = deepcopy(post_data)
        shop_id = request.data['shopkeeper']
        giftSpin = request.data['giftSpin']
        user = User.objects.get(id=shop_id)
        shopkeeper_obj = Shopkeeper.objects.get(user_id=user.id)
        post_Data['shopkeeper'] = shopkeeper_obj.id
        serializer = WinSpinSerializer(data=post_Data)
        if serializer.is_valid():
            serializer.save()
            giftSpin = GiftSpin.objects.get(id=giftSpin)
            qty = giftSpin.quantity
            newQty = qty - 1
            giftSpin.quantity = newQty
            giftSpin.save()

            spins_obj = Spines.objects.filter(shopkeeper=shopkeeper_obj.id)
            if spins_obj:
                spin_count = spins_obj[0].spine_no
                total_spin = spin_count - 1
                spins_obj[0].spine_no = total_spin
                spins_obj[0].save()

            response = {
                'message': 'You have successfully win the Spin'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)

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
            token = token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24)},
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


class NotificationViewSetApi(viewsets.ViewSet):

    def list(self, request):
        # tokenCheck(request)
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ComplaintsViewSetApi(viewsets.ViewSet):

    # def list(self, request):
    #     tokenCheck(request)
    #     gifts = GiftSpin.objects.filter(quantity__gt=0)
    #     serializer = GiftSpineSerializer(gifts, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        tokenCheck(request)

        post_data = request.data
        post_data=deepcopy(request.data)
        user_id = request.data['userId']
        try:
            shopkeeper_obj = Shopkeeper.objects.get(user=user_id)
            comp =Complaints.objects.create(shopkeeper=shopkeeper_obj, message=post_data['message'])
            comp.save()
            response = {
                'message': 'Your Complaints has been register '
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Shopkeeper.DoesNotExist:
            try:
                employee_obj = Employee.objects.get(user=user_id)

                comp = Complaints.objects.create(employee=employee_obj, message=post_data['message'])
                comp.save()
                response = {
                    'message': 'Your Complaints has been register '
                }
                return Response(response, status=status.HTTP_201_CREATED)
            except Employee.DoesNotExist:
                customer_obj = Customer.objects.get(user=user_id)
                comp = Complaints.objects.create(customer=customer_obj, message=post_data['message'])
                comp.save()
                response = {
                    'message': 'Your Complaints has been register '
                }
                return Response(response, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):
        tokenCheck(request)
        try:
            shopkeeper_obj = Shopkeeper.objects.get(user=pk)
            
            complaints_list = Complaints.objects.filter(shopkeeper_id=shopkeeper_obj.id)
            
            serializer = ComplaintSerializer(complaints_list, many=True)
         
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Shopkeeper.DoesNotExist:
            try:
                Employee_obj = Employee.objects.get(user=pk)
                complaints_list = Complaints.objects.filter(employee_id=Employee_obj.id)
               
                serializer = ComplaintSerializer(complaints_list, many=True)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                customer_obj = Customer.objects.get(user=pk)
                complaints_list = Complaints.objects.filter(customer_id=customer_obj.id)
                
                serializer = ComplaintSerializer(complaints_list, many=True)
               
                return Response(serializer.data, status=status.HTTP_200_OK)


# class ChangePasswordView(generics.UpdateAPIView):

#     print('req', request)
#     """
#     An endpoint for changing password.
#     """
#     print('request', request)
#     serializer_class = ChangePasswordSerializer

#     # model = User
#     # permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

