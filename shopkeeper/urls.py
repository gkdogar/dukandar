from django.urls import path
from dukandar import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [

    path('', index, name='index'),
    path('register', register, name='register'),
    path('customer/List', EmployeeListView.as_view(), name='employee_List'),

    path('customer/setup', EmployeeSetupView.as_view(), name='employee_setup'),
    path('parent/category/setup', ParentCategorySetupView.as_view(), name='parent_category_setup'),
]
