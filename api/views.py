from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from shopkeeper.models.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, \
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly



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

class EmployeeViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            employee = Employee.objects.all()
            if employee:
                # user = request.user
                # if user is not None:
                #     users = User.objects.filter(email=user)
                # else:
                #     users = User.objects.all()
                print('user is>> ', employee)
                serializer = EmployeeSerializer(employee, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response = {
                    'message': 'Employee Does Not Exist'
                }
                return Response(response, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            response = {
                'message': 'Employee Does Not Exist'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        print('hello', request.data)
        serializer = EmployeeSerializer(data=request.POST)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Record Created successfully.'

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
