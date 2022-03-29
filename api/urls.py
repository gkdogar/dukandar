from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# router.register('user', views.UserRegister,basename='user')
# router.register('account/registration', views.userRegistration,basename='registration')

router.register('dukandar', views.ShopkeeperViewSetApi, basename='dukandar')
router.register('customer', views.CustomerViewSetApi, basename='customers')
router.register('parent/category/list', views.ParentCategoryView, basename='parentCategory')
router.register('parent/sub/category/list', views.SubCategoryView, basename='subCategory')
router.register('products/list', views.ProductViewSetApi, basename='products')
router.register('all/products/list', views.AllProductApi, basename='allproducts')
router.register('orders', views.OrderViewSetApi, basename='orders')
router.register('wallet', views.WalletViewSetApi, basename='wallet')
router.register('spines', views.SpinesViewSetApi, basename='spines')
router.register('employee', views.EmployeeViewSetApi, basename='employee')
router.register('gift/spin', views.GiftSpineViewSetApi, basename='giftspin')
router.register('notification/user', views.NotificationViewSetApi, basename='notifications')
router.register('complaints/user', views.ComplaintsViewSetApi, basename='complaints')

# router.register('login', views.LoginAPI.as_view(),basename='Login_User')
app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    # path('api/gettoken/', obtain_auth_token)
    # path('account/registration/', views.userRegistration,name='registration '),
    # path('loginToken/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/user', views.LoginAPI.as_view(), name='login_user'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
    # path('product/', views.ProductAPIVIEW.as_view(), name='product_'),
    # path('product/<int:pk>/', views.ProductAPIVIEW.as_view(), name='product_api'),
    path('loginapi/user', views.LoginView.as_view(), name='login_view'),
    path('user', views.UserView.as_view(), name='UserView_view'),
    path('user/logout', views.LogoutView.as_view(), name='logoutView'),
    # path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
