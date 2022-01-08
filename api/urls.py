from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router=DefaultRouter()
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# router.register('user', views.UserRegister,basename='user')
router.register('shopkeeper_setup', views.UserRegister,basename='shopkeeper_setup')
router.register('shopkeeper_list', views.UserRegister,basename='shopkeeper_list')
router.register('customer_setup', views.UserRegister,basename='customer_setup')
router.register('customer_list', views.UserRegister,basename='customer_list')
router.register('discount_products', views.UserRegister,basename='discount_products')
router.register('spins ', views.UserRegister,basename='spins ')


app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    # path('api/gettoken/', obtain_auth_token)
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),

]
