from django.urls import path
from dukandar import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('', index, name='index'),
    path('register', register, name='register'),
    path('customer/List', EmployeeListView.as_view(), name='employee_List'),
    path('google/map/pins/', google_map, name='google_map_pin'),
    path('customer/setup', EmployeeSetupView.as_view(), name='employee_setup'),
    # Parent_categorie+URLS
    path('parent/category/setup', ParentCategorySetupView.as_view(), name='parent_category_setup'),
    path('parent/category/lists', parent_category_list, name='parent_category_list'),
    path('parent/category/setup/<int:pk>/', parent_category_detail, name='parent_category_update'),
    path('parent/category/delete/<int:pk>/', parent_category_delete, name='parent_category_delete'),

]
