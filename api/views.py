from numpy import product
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from shopkeeper.models.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, \
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly


class EmployeeViewSetApi(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # def list(self, request):
    #     print('list Employee')
    #     employees = Employee.objects.all()
    #     serializer = EmployeeSerializer(employees, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            employee = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        print('create Employee', request.POST)
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        print("********List*******")
        print("BaseName:>>", self.basename)
        print("action:>>", self.action)
        print("detail:>>", self.detail)
        print("suffix:>>", self.suffix)
        print("description:>>", self.description)
        print("description:>>", self.description)
        id = pk
        employee = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        id = pk
        employee = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Partial Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        employee = Employee.objects.get(id=pk)
        employee.delete()
        response = {
            'message': 'Record Deleted Successfully'
        }
        return Response(response, status=status.HTTP_200_OK)

class ShopkeeperViewSetApi(viewsets.ViewSet):
    # def list(self, request):
    #     dukandar = Shopkeeper.objects.all()
    #     serializer = ShopkeeperSerializer(dukandar, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            dukandar = Shopkeeper.objects.get(id=id)
            serializer = ShopkeeperSerializer(dukandar)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        print('POST Request API', request.POST)
        print('POST Request Data', request.data)
        serializer = ShopkeeperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            e
            print('Invalid Serializer')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        print("********List*******")
        print("BaseName:>>", self.basename)
        print("action:>>", self.action)
        print("detail:>>", self.detail)
        print("suffix:>>", self.suffix)
        print("description:>>", self.description)
        print("description:>>", self.description)
        id = pk
        dukandar = Shopkeeper.objects.get(id=id)
        serializer = ShopkeeperSerializer(dukandar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        id = pk
        dukandar = Shopkeeper.objects.get(id=id)
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

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        print("********List*******")
        print("BaseName:>>", self.basename)
        print("action:>>", self.action)
        print("detail:>>", self.detail)
        print("suffix:>>", self.suffix)
        print("description:>>", self.description)
        print("description:>>", self.description)
        id = pk
        customer = Customer.objects.get(id=id)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        id = pk
        customer = Customer.objects.get(id=id)
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
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        print("********List*******")
        print("BaseName:>>", self.basename)
        print("action:>>", self.action)
        print("detail:>>", self.detail)
        print("suffix:>>", self.suffix)
        print("description:>>", self.description)
        print("description:>>", self.description)
        id = pk
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Complete Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        id = pk
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Partial Record Update Successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        product = Product.objects.get(id=pk)
        product.delete()
        response = {
            'message': 'Record Deleted Successfully'
        }
        return Response(response, status=status.HTTP_200_OK)

class UserRegister(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user =request.user
        if user is not None:
            users =User.objects.filter(email=user)
        else:
            users = User.objects.all()
        print('user is>> ',users)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Record Created Successfully !'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            print('hello',request.data)
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

@api_view(['POST',])
def userRegisstration(request):
    print('req', request)
    if request.method=='POST':
        serializers=UserRegistrationSerializer(data=request.POST)
        data={}
        if serializers.is_valid():
            user =serializers.save()
            data['response']='Record Created successfully.'
            data['email'] = user.email
            data['username'] = user.username
        else:
            data=serializers.errors
        return Response(data)
    else:
        return Response('Get')

