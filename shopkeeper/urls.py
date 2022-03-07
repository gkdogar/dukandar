from django.urls import path
from dukandar import settings
from django.conf.urls.static import static
from .views import *
app_name = 'shopkeeper'
urlpatterns = [

    path('', dashboard, name='dashboard'),
    path('login', admin_login, name='admin_login'),
    path('settings', admin_settings, name='admin_setting'),
    path('register', register, name='register'),
    path('google/map/pins/', google_map, name='google_map_pin'),


    # Employee+URLS
    path('employee/lists', employeeList, name='employee_list'),
    path('employee/history/lists', employeeHistoryList, name='employee_history'),
    path('employee/setup', employeeSetup, name='employee_setup'),
    path('employee/setup/<int:pk>/', employeeUpdate, name='employee_update'),
    path('employee/delete/<int:pk>/', employeeDelete, name='employee_delete'),

    #Dukandar+URLS
    path('dukandar/setups',dukandarSetup, name='dukandar_setup'),
    path('dukandar/lists', dukandarList, name='dukandar_list'),
    path('dukandar/setup/<int:pk>/', dukandarUpdate, name='dukandar_update'),
    path('dukandar/delete/<int:pk>/', dukandarDelete, name='dukandar_delete'),

    #Customer+URLS
    path('customer/setup', customerSetup, name='customer_setup'),
    path('customer/lists', customerList, name='customer_list'),
    path('customer/setup/<int:pk>/', customerDetail, name='customer_update'),
    path('customer/delete/<int:pk>/', customerDelete, name='customer_delete'),


    # Parent_categorie+URLS
    path('parent/category/lists', parent_category_list, name='parent_category_list'),
    path('parent/category/setup', ParentCategorySetupView.as_view(), name='parent_category_setup'),
    path('parent/category/setup/<int:pk>/', parent_category_detail, name='parent_category_update'),
    path('parent/category/delete/<int:pk>/', parent_category_delete, name='parent_category_delete'),

    # Parent_Sub_categorie+URLS
    path('parent/sub/category/setup', sub_categorySetup, name='parent_sub_category_setup'),
    path('parent/sub/category/lists', sub_categoryList, name='parent_sub_category_list'),
    path('parent/sub/category/setup/<int:pk>/', sub_categoryUpdate, name='parent_sub_category_update'),
    path('parent/sub/category/delete/<int:pk>/', sub_categoryDelete, name='parent_sub_category_delete'),

    # Product+URLS
    path('product/lists', productList, name='product_list'),
    path('product/setup', productSetup, name='product_setup'),
    path('product/setup/<int:pk>/', productUpdate, name='product_update'),
    path('product/delete/<int:pk>/', productDelete, name='product_delete'),

    # Order+URLS
    path('Order/lists', ordersList, name='orders_list'),
    path('Order/lists/detail/<int:pk>/', ordersDetails, name='order_details'),
    path('Order/lists/delete/<int:pk>/', ordersDelete, name='order_delete'),
    # wallet+URLS
    path('wallet/lists', walletList, name='wallet_list'),

    # wallet+URLS
    path('spines/lists', spinesList, name='spines_list'),

    path('parent/sub/category/ajax/lists/', parent_sub_ajax_data, name='parent_sub_ajax_data'),
    path('logout', admin_logout, name='admin_logout'),

    # //Gifts 
    path('gift/lists', giftList, name='gift_List'),
    path('gift/setup', giftSetup, name='gift_Setup'), 
      path('gift/detail/<int:pk>/', giftDetails, name='gift_detail'),
    path('gift/delete/<int:pk>/', giftDelete, name='gift_delete'),
   # OrderHistory+URLS
    path('Order/history/lists', ordersHistoryList, name='orders_history_list'),
    path('Order/history/detail/<int:pk>/', ordersHistoryDetails, name='order_history_details'),
]
