from django.shortcuts import render, redirect
from bootstrap_modal_forms.generic import BSModalCreateView
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models.models import *
from django.views import View
from django.views.generic import ListView, View
from django.contrib import messages
import folium
import pandas as pd
import re
from django.core.mail import send_mail, BadHeaderError
from decouple import config
from datetime import datetime, timedelta
from time import gmtime
from time import strftime
import reportlab
from .utils import *
from django.http import JsonResponse
import json
# from .utils import *
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse


EMAIL_HOST_USER = config('EMAIL_HOST_USER')


from django.template.loader import get_template


def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        email_user = authenticate(email=email, password=password)
      
        if email_user:
            check_user = User.objects.filter(email=email_user)
            if (email is None) or (password is None):
                messages.error(request, "Email or Password not given")
                return redirect('shopkeeper:admin_login')
            elif (password is None) and (email is None):
                messages.error(request, "Credentials can't be empty")
                return redirect('shopkeeper:admin_login')
            else:
                if email_user.user_type == 'SUPER_ADMIN':
                    login(request, email_user)

                    return redirect('shopkeeper:dashboard')

                messages.error(request, "You are Not Admin ! Sorry You Can't Login ")
                return redirect('shopkeeper:admin_login')

        else:
            messages.add_message(request, messages.ERROR, 'Email or Password not Given')
            return redirect('shopkeeper:admin_login')
    else:
        return render(request, 'shopkeeper/registration/login.html')


@login_required(login_url='shopkeeper:admin_login')
def admin_settings(request):
    if request.POST:
        user = User.objects.get(id=request.user.id)

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.city = request.POST.get('city')
        user.phone_no = request.POST.get('phone_no')
        user.address = request.POST.get('address')
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
        return redirect('shopkeeper:admin_setting')
    else:
        user = User.objects.get(id=request.user.id)
        context = {
            'user': user
        }
        return render(request, 'shopkeeper/settings.html', context)


@login_required(login_url='shopkeeper:admin_login')
def dashboard(request):
    employees = Employee.objects.all().count()
    customers = Customer.objects.all().count()
    dukandars_list = Shopkeeper.objects.all()
    dukandars = dukandars_list.count()
    products = Product.objects.all().count()
    orders = Order.objects.all().count()
    total_order = Order.objects.filter(status='DELIVERED')
    toal_sale = 0
    # /// Wallet will be Zero  start /
    current_date = datetime.now()
    first_date_month = current_date.replace(day=1)
    if current_date.date() == first_date_month.date():
        walt_obj = Wallet.objects.all()
        for wlt in walt_obj:
            wlt.amount = 0
            wlt.save()
    # /// Wallet will be Zero End
    for t in total_order:
        toal_sale += t.total_amount

    locationlist = []
    map = folium.Map(location=[31.5204, 74.3587], zoom_start=12)
    df_counters = pd.DataFrame(list(Shopkeeper.objects.all().values('latitude', 'longitude', 'shop_name')))
    if not df_counters.empty:
        locations = df_counters[['latitude', 'longitude']]
        locationlist = locations.values.tolist()
        for point in range(0, len(locationlist)):
            folium.Marker(locationlist[point], popup=df_counters['shop_name'][point],
                          tooltip=df_counters['shop_name'][point]).add_to(map)

    # folium.Marker(location=[31.5047, 74.3315], popup='Default popup Marker1',
    #               tooltip='Click here to see Popup').add_to(map)
    # folium.Marker(location=[31.511996, 74.343018], popup='Default popup Marker1',
    #               tooltip='Click here to see Popup').add_to(map)

    map = map._repr_html_()
    context = {
        'employees': employees,
        'dukandars': dukandars,
        'customers': customers,
        'products': products,
        'orders': orders,
        'map': map,
        'toal_sale': toal_sale

    }
    return render(request, 'shopkeeper/dashboard.html', context)


def employee_target(employee_list):
    for emp in employee_list:
        target_add_date = emp.updated_at
        current_date = datetime.today()
        created_at__gt = datetime.today() + timedelta(days=1)
        if target_add_date.date() < current_date.date():
            emp_histroy = EmployeeHistry.objects.create(employee=emp, daily_target_assign=emp.target_assign,
                                                        daily_achieved=emp.target_achieved)
            emp_histroy.save()
            emp.target_achieved = 0
            emp.save()
            print('hello')


@login_required(login_url='shopkeeper:admin_login')
def employeeList(request):
    employee_list = Employee.objects.all()
    # for emp in employee_list:
    #     emp.removeTarget()
    context = {
        'employee_list': employee_list
    }
    return render(request, 'shopkeeper/employee/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def employeeHistoryList(request):
    employee_history_list = EmployeeHistry.objects.all()
    context = {
        'employee_history_list': employee_history_list
    }
    return render(request, 'shopkeeper/employee/history.html', context)


@login_required(login_url='shopkeeper:admin_login')
def employeeSetup(request):
    if request.POST:

        employee_id = request.POST.get('employee_id') or None
        if employee_id:
            employee_obj = Employee.objects.get(id=employee_id)
            user = User.objects.get(id=employee_obj.user.id)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.address = request.POST.get('address')
            user.city = request.POST.get('city')
            user.phone_no = request.POST.get('phone_no')
            user.save()
            employee_obj.user = user

            employee_obj.description = request.POST.get('description')
            employee_obj.target_assign = request.POST.get('target_assign')
            employee_obj.target_achieved = request.POST.get('target_achieved')
            employee_obj.area_designated = request.POST.get('area_designated')
            employee_obj.is_active = request.POST.get('is_active') or False
            employee_obj.save()
            emp_histroy = EmployeeHistry.objects.create(employee=employee_obj,
                                                        daily_target_assign=employee_obj.target_assign,
                                                        daily_achieved=employee_obj.target_achieved)
            emp_histroy.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            return redirect('shopkeeper:employee_list')

        else:

            email = request.POST.get('email')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            check_user = User.objects.filter(email=email)
            if check_user.count() == 1:
                messages.error(request, 'UserName Already Existed')
                return redirect('shopkeeper:employee_setup')
            if password != password1:
                reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
                pat = re.compile(reg)
                mat = re.search(pat, password)
                if mat:
                    print("Password is valid.")
                else:
                    messages.error(request, 'Password Must contains one Capital and One Speceial Char')
                    return redirect('shopkeeper:employee_setup')
                messages.error(request, 'Password must be matched!')
                return redirect('shopkeeper:employee_setup')
            user = User.objects.create_user(email=email, password=password)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.address = request.POST.get('address')
            user.city = request.POST.get('city')
            user.phone_no = request.POST.get('phone_no')
            user.user_type = 'STAFF'
            employee = Employee.objects.create(user=user,
                                               target_assign=request.POST.get('target_assign'),
                                               target_achieved=request.POST.get('target_achieved'),
                                               area_designated=request.POST.get('area_designated'),
                                               description=request.POST.get('description'),
                                               is_active=request.POST.get('is_active') or False)
            employee.save()
            emp_histroy = EmployeeHistry.objects.create(employee=employee, daily_target_assign=employee.target_assign,
                                                        daily_achieved=employee.target_achieved)
            emp_histroy.save()
            user.save()
            messages.success(request, 'Record Created Successfully')
            return redirect('shopkeeper:employee_list')
    else:

        return render(request, 'shopkeeper/employee/setup.html')


@login_required(login_url='shopkeeper:admin_login')
def employeeUpdate(request, pk):
    employee_obj = Employee.objects.get(id=pk)
    context = {
        'employee_id': employee_obj.id,
        'user': employee_obj.user,
        'target_assign': employee_obj.target_assign,
        'target_achieved': employee_obj.target_achieved,
        'description': employee_obj.description,
        'area_designated': employee_obj.area_designated,
        'is_active': employee_obj.is_active,
    }

    return render(request, 'shopkeeper/employee/setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def employeeDelete(request, pk):
    employee_obj = Employee.objects.get(id=pk)
    user_obj = User.objects.get(id=employee_obj.user.id)
    employee_obj.delete()
    user_obj.delete()
    messages.add_message(request, messages.SUCCESS, 'Record Deleted Successfully')
    return redirect('shopkeeper:employee_list')


@login_required(login_url='shopkeeper:admin_login')
def dukandarList(request):
    dukandars_list = Shopkeeper.objects.all()
    order_list = []
    walet_list = []
    spines_list = []
    winSpin_list = []

    for dukan in dukandars_list:
        order_li = Order.objects.filter(shopkeeper=dukan.id)
        for ord in order_li:
            order_list.append({
                'id': ord.id,
                'amount': ord.total_amount,
                'shopkeeper': ord.shopkeeper
            })
        walet_li = Wallet.objects.filter(shopkeeper=dukan.id)
        for wlt in walet_li:
            walet_list.append({
                'id': wlt.id,
                'amount': wlt.amount,
                'shopkeeper': wlt.shopkeeper
            })
        spines_li = Spines.objects.filter(shopkeeper=dukan.id)
        for spin in spines_li:
            spines_list.append({
                'id': spin.id,
                'amount': spin.order,
                'spine_no': spin.spine_no,
                'shopkeeper': spin.shopkeeper
            })

        winspin_list = WinSpin.objects.filter(shopkeeper=dukan.id)
        for spin in winspin_list:
            winSpin_list.append({
                'id': spin.id,
                'shopkeeper': spin.shopkeeper,
                'giftspins': spin.giftSpin,

            })

    context = {
        'dukandars_list': dukandars_list,
        'order_list': order_list,
        'walet_list': walet_list,
        'spines_list': spines_list,
        'winSpin_list': winSpin_list
    }
    return render(request, 'shopkeeper/dukandar/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def dukandarSetup(request):
    if request.POST:
        print('shopkeeper_type', request.POST.get('shopkeeper_type'))
        dukandar_id = request.POST.get('dukandar_id') or None
        dukandar_obj = Shopkeeper.objects.get(id=dukandar_id)
        print('dukandar_obj', dukandar_obj)
        user = User.objects.get(id=dukandar_obj.user.id)

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.address = request.POST.get('address')
        user.city = request.POST.get('city')
        user.phone_no = request.POST.get('phone_no')
        user.save()
        dukandar_obj.user = user
        dukandar_obj.shop_name = request.POST.get('shop_name')
        dukandar_obj.shopkeeper_type = request.POST.get('shopkeeper_type')
        dukandar_obj.description = request.POST.get('description')
        # dukandar_obj.latitude=request.POST.get('first_name')
        # dukandar_obj.longitude=request.POST.get('first_name')
        dukandar_obj.is_active = request.POST.get('is_active') or False
        dukandar_obj.save()
        messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
        return redirect('shopkeeper:dukandar_list')
    else:
        return render(request, 'shopkeeper/dukandar/setup.html')


@login_required(login_url='shopkeeper:admin_login')
def dukandarUpdate(request, pk):
    dukandar_obj = Shopkeeper.objects.get(id=pk)
    context = {
        'dukandar_id': dukandar_obj.id,
        'emp_id': dukandar_obj.emp_id,
        'user': dukandar_obj.user,
        'shop_name': dukandar_obj.shop_name,
        'shopkeeper_type': dukandar_obj.shopkeeper_type,
        'description': dukandar_obj.description,
        'is_active': dukandar_obj.is_active,
    }
    return render(request, 'shopkeeper/dukandar/setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def dukandarDelete(request, pk):
    dukandar_obj = Shopkeeper.objects.get(id=pk)
    user_obj = User.objects.get(id=dukandar_obj.user.id)
    dukandar_obj.delete()
    user_obj.delete()

    messages.add_message(request, messages.SUCCESS, 'Record Deleted Successfully')
    return redirect('shopkeeper:dukandar_list')


@login_required(login_url='shopkeeper:admin_login')
def customerSetup(request):
    if request.POST:
        customer_id = request.POST.get('id') or None
        if customer_id:
            customer_obj = Customer.objects.get(id=customer_id)
            user = User.objects.get(id=customer_obj.user.id)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.address = request.POST.get('address')
            user.city = request.POST.get('city')
            user.phone_no = request.POST.get('phone_no')
            user.save()
            customer_obj.user = user
            print('dd',request.POST.get('is_active'))
            customer_obj.is_active = request.POST.get('is_active') or False

            customer_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            return redirect('shopkeeper:customer_list')

        else:

            email = request.POST.get('email')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            check_user = User.objects.filter(email=email)
            if check_user.count() == 1:
                messages.error(request, 'UserName Already Existed')
                return redirect('shopkeeper:customer_setup')
            if password != password1:
                reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
                pat = re.compile(reg)
                mat = re.search(pat, password)
                if mat:
                    print("Password is valid.")
                else:
                    messages.error(request, 'Password Must contains one Capital and One Speceial Char')
                    return redirect('shopkeeper:employee_setup')
                messages.error(request, 'Password must be matched!')
                return redirect('shopkeeper:customer_setup')
            user = User.objects.create_user(email=email, password=password)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.address = request.POST.get('address')
            user.user_type = 'CUSTOMER'
            customer = Customer.objects.create(user=user, phone_no=request.POST.get('phone_no'),
                                               is_active=request.POST.get('is_active') or False)
            customer.save()
            user.save()
            messages.success(request, 'Record Created Successfully')
            return redirect('shopkeeper:customer_list')
    else:
        return render(request, 'shopkeeper/customer/setup.html')


@login_required(login_url='shopkeeper:admin_login')
def customerList(request):
    customer_list = Customer.objects.all()
    order_list = []
    for customer in customer_list:
        order_li = Order.objects.filter(customer=customer.id)
        for ord in order_li:
            order_list.append({
                'id': ord.id,
                'amount': ord.total_amount,
                'customer': ord.customer
            })
    context = {
        'customer_list': customer_list,
        'order_list': order_list
    }
    return render(request, 'shopkeeper/customer/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def customerDetail(request, pk):
    if request.POST:
        pass
    else:
        customer = Customer.objects.get(id=pk)
        user = User.objects.get(customer=pk)
        context = {
            'customer': customer,
            'id': pk,

        }
        return render(request, 'shopkeeper/customer/setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def customerDelete(request, pk):
    customer_obj = User.objects.get(customer=pk)
    customer_obj.delete()
    messages.add_message(request, messages.SUCCESS, 'Record Deleted Successfully')
    return redirect('shopkeeper:customer_list')
    return render(request, 'shopkeeper/customer/setup.html')


# class CustomerSetupView(BSModalCreateView):
#     template_name = 'shopkeeper/customer/setup.html'
#     form_class = EmployeeModelForm
#     success_message = 'Success: Book was created.'
#     success_url = reverse_lazy('index')
@login_required(login_url='shopkeeper:admin_login')
def parent_category_list(request):
    parent_list = ParentCategory.objects.all()
    context = {
        'parent_list': parent_list
    }
    return render(request, 'shopkeeper/parent/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def parent_category_detail(request, pk):
    parent_obj = ParentCategory.objects.get(id=pk)
    context = {
        'paren_id': parent_obj.id,
        'name': parent_obj.name,
        'description': parent_obj.description,
        'meta_keywords': parent_obj.meta_keywords,
        'meta_description': parent_obj.meta_description,
        'image': parent_obj.image,
        'category_for': parent_obj.category_for,
        'is_active': parent_obj.is_active,
    }
    return render(request, 'shopkeeper/product/parent_category_setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def parent_category_delete(request, pk):
    
    parent_delete = ParentCategory.objects.get(id=pk)
    parent_delete.delete()
    messages.success(request, 'Record Deleted Successfully')
    return redirect('shopkeeper:parent_category_list')


class ParentCategorySetupView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'shopkeeper/parent/setup.html')

    def post(self, request, *args, **kwargs):

        paren_id = request.POST.get('paren_id') or None
        if paren_id:
            parent_obj = ParentCategory.objects.get(id=paren_id)
            img = parent_obj.image
            parent_obj.name = request.POST.get('name')
            parent_obj.description = request.POST.get('description')
            parent_obj.meta_keywords = request.POST.get('meta_keywords')
            parent_obj.meta_description = request.POST.get('meta_description')
            parent_obj.image = request.FILES.get('image') or img
            parent_obj.is_active = request.POST.get('is_active') or False
            parent_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            return redirect('shopkeeper:parent_category_list')
        else:
            form = ParentCategoryForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Created Successfully')
                return redirect('shopkeeper:parent_category_list')
            else:
                messages.error(request, 'Something Went Wrong')
                return redirect('shopkeeper:parent_category_setup')


@login_required(login_url='shopkeeper:admin_login')
def sub_categoryList(request):
    sub_category_list = SubCategory.objects.all()
    context = {
        'sub_category_list': sub_category_list
    }
    return render(request, 'shopkeeper/sub/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def sub_categorySetup(request):
    if request.POST:
        sub_id = request.POST.get('sub_id') or None
        if sub_id:
            sub_obj = SubCategory.objects.get(id=sub_id)
            img = sub_obj.image
            sub_obj.parent = ParentCategory.objects.get(id=request.POST.get('parent'))
            sub_obj.name = request.POST.get('name')
            sub_obj.description = request.POST.get('description')
            sub_obj.meta_keywords = request.POST.get('meta_keywords')
            sub_obj.meta_description = request.POST.get('meta_description')
            sub_obj.image = request.FILES.get('image') or img
            sub_obj.is_active = request.POST.get('is_active') or False
            sub_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            return redirect('shopkeeper:parent_sub_category_list')

        else:
            form = SubCategoryForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Created Successfully')
                return redirect('shopkeeper:parent_sub_category_list')
            else:
                messages.error(request, 'Something Went Wrong')
                return redirect('shopkeeper:parent_sub_category_setup')
    else:
        parent_cat_list = ParentCategory.objects.filter(is_active=True)
        context = {
            'parent_cat_list': parent_cat_list
        }
        return render(request, 'shopkeeper/sub/setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def sub_categoryUpdate(request, pk):
    sub_obj = SubCategory.objects.get(id=pk)
    parent_cat_list = ParentCategory.objects.all()
    context = {
        'parent_cat_list': parent_cat_list,
        'sub_id': sub_obj.id,
        'parent_id': sub_obj.parent.id,
        'name': sub_obj.name,
        'description': sub_obj.description,
        'meta_keywords': sub_obj.meta_keywords,
        'meta_description': sub_obj.meta_description,
        'image': sub_obj.image,
        'is_active': sub_obj.is_active,
    }
    return render(request, 'shopkeeper/sub/setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def sub_categoryDelete(request, pk):
    sub_obj = SubCategory.objects.get(id=pk)
    sub_obj.delete()
    messages.success(request, 'Record Deleted Successfully')
    return redirect('shopkeeper:parent_sub_category_list')


@login_required(login_url='shopkeeper:admin_login')
def productList(request):
    products_list = Product.objects.all()
    context = {
        'products_list': products_list
    }
    return render(request, 'shopkeeper/product/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def productSetup(request):
    if request.POST:
        product_id = request.POST.get('product_id') or None
        if product_id:
            prod_obj = Product.objects.get(id=product_id)
            img = prod_obj.image
            prod_obj.parent = ParentCategory.objects.get(id=request.POST.get('parent'))
            prod_obj.sub_cat = SubCategory.objects.get(id=request.POST.get('sub_cat'))
            prod_obj.name = request.POST.get('name')
            prod_obj.description = request.POST.get('description')
            prod_obj.r_price = request.POST.get('r_price')
            prod_obj.w_price = request.POST.get('w_price')
            prod_obj.quantity = request.POST.get('quantity')
            prod_obj.discount = request.POST.get('discount')
            prod_obj.image = request.FILES.get('image') or img
            prod_obj.is_active = request.POST.get('is_active') or False
            prod_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            return redirect('shopkeeper:product_list')
        else:
            form = ProductForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Created Successfully')
                return redirect('shopkeeper:product_list')
            else:
                print('Form Error', form.errors)
                messages.error(request, 'Something Went Wrong')
                return redirect('shopkeeper:product_setup')

    else:
        parent_cat_list = ParentCategory.objects.filter(is_active=True)
        parent_sub_list = SubCategory.objects.filter(is_active=True)
        context = {
            'parent_cat_list': parent_cat_list,
            'parent_sub_list': parent_sub_list
        }
        return render(request, 'shopkeeper/product/setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def productUpdate(request, pk):
    prod_obj = Product.objects.get(id=pk)
    parent_cat_list = ParentCategory.objects.filter(is_active=True)
    parent_sub_list = SubCategory.objects.filter(is_active=True)
    context = {
        'parent_cat_list': parent_cat_list,
        'parent_sub_list': parent_sub_list,
        'product_id': prod_obj.id,
        'parent_id': prod_obj.parent.id,
        'sub_cat_id': prod_obj.sub_cat.id,
        'name': prod_obj.name,
        'image': prod_obj.image,
        'description': prod_obj.description,
        'quantity': prod_obj.quantity,
        'r_price': prod_obj.r_price,
        'w_price': prod_obj.w_price,
        'discount': prod_obj.discount,
        'is_active': prod_obj.is_active,
    }
    return render(request, 'shopkeeper/product/setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def productDelete(request, pk):
    prod_obj = Product.objects.get(pk=pk)  
    prod_obj.delete()
    messages.success(request, 'Record Deleted Successfully')
    return redirect('shopkeeper:product_list')


@login_required(login_url='shopkeeper:admin_login')
def ordersList(request):
    orders_list = Order.objects.all()
    shopkeeper = None
    customer = None
    for order in orders_list:
        shopkeeper = order.shopkeeper
        customer = order.customer
    print('shopkeeper', customer)
    context = {
        'orders_list': orders_list,
        'shopkeeper': shopkeeper,
        'customer': customer
    }
    return render(request, 'shopkeeper/order/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def ordersDetails(request, pk):
    if request.POST:
        pdf = request.POST.get('PDF_BTN', None)

        if pdf:
            orders_obj = Order.objects.filter(id=pdf)

            orders_obj = Order.objects.get(id=pdf)
            shopkeeper_obj = orders_obj.shopkeeper or None
            customer_obj = orders_obj.customer or None
            product_orders = ProductOrder.objects.filter(order_id=pk)
            # win_gift=WinSpin.objects.filter(shopkeeper_id=shopkeeper_obj.id)

            context = {
                'order_id': orders_obj.id,
                'products': product_orders,
                'dukandar': orders_obj.shopkeeper,
                'customer': orders_obj.customer,
                'order_date': orders_obj.created_at,
                'amount': orders_obj.total_amount,
                'discount': orders_obj.discount,
                'order_upto': orders_obj.order_upto,
                'shopkeeper_obj': shopkeeper_obj,
                'customer_obj': customer_obj,
                # 'win_gift_list':win_gift,

                'status': orders_obj.status,
            }

            pdf = render_to_pdf('shopkeeper/pdf.html', context)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="dukandarOrder#' + str(orders_obj.id) + '".pdf"'
            return response

        else:
            orders_obj = Order.objects.get(id=pk)
            orders_obj.status = request.POST['status']
            orders_obj.save()
            ord_hist = OrderHistory.objects.create(order=orders_obj)
            ord_hist.status = orders_obj.status
            ord_hist.save()
            messages.success(request, 'Order Status Updated Successfully')
            return redirect('shopkeeper:orders_list')
    else:

        orders_obj = Order.objects.get(id=pk)
        product_orders = ProductOrder.objects.filter(order_id=pk)
        shopkeeper_id = orders_obj.shopkeeper or None
        customer_id = orders_obj.customer or None
        context = {
            'order_id': orders_obj.id,
            'products': product_orders,
            'dukandar': orders_obj.shopkeeper,
            # 'customer':orders_obj.customer,
            'order_date': orders_obj.created_at,
            'amount': orders_obj.total_amount,
            'discount': orders_obj.discount,
            'order_upto': orders_obj.order_upto,
            'shopkeeper_id': shopkeeper_id,
            'customer_id': customer_id,

            'status': orders_obj.status,

        }
        return render(request, 'shopkeeper/order/detail.html', context)


def ordersDelete(request, pk):
    orders_obj = Order.objects.get(id=pk)
    product_ord = ProductOrder.objects.filter(order_id=pk)
    product_ord.delete()
    orders_obj.delete()
    messages.success(request, 'Order Deleted Successfully')
    return redirect('shopkeeper:orders_list')


@login_required(login_url='shopkeeper:admin_login')
def walletList(request):
    wallet_list = Wallet.objects.all()
    context = {
        'wallet_list': wallet_list,
    }
    return render(request, 'shopkeeper/wallet/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def spinesList(request):
    spine_list = Spines.objects.all()
    context = {
        'spine_list': spine_list,
    }
    return render(request, 'shopkeeper/spins/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def register(request):
    if request.method == 'POST':
        print('request post', request.POST)
        form = ExtendUserCreationForm(request.POST)
        shopkeeper_form = ShopkeeperForm(request.POST)
        if form.is_valid() and shopkeeper_form.is_valid():
            user = form.save()
            print('user >', user)
            user.user_type = 'SHOPKEEPER'
            print('userId >', user.id)
            shopkeeper = shopkeeper_form.save(commit=False)
            shopkeeper.user = user
            shopkeeper.save()
            print('shopkeeper', shopkeeper)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.add_message(request, messages.SUCCESS, 'Record Update Successfuly')
            return redirect('shopkeeper:index')
        else:
            print('Form Error')
            print(form.errors)
            messages.add_message(request, messages.ERROR, 'Form has an error existed')




    else:
        form = ExtendUserCreationForm()
        shopkeeper_form = ShopkeeperForm()
    context = {
        'form': form,
        'shopkeeper_form': shopkeeper_form
    }
    return render(request, 'shopkeeper/dukandar/setup.html', context)


@login_required(login_url='shopkeeper:admin_login')
def google_map(request):
    locationlist = []
    # for point in range(0, len(locationlist)):
    #     folium.Marker(locationlist[point], popup=df_counters['Name'][point]).add_to(map)

    m = folium.Map(location=[31.5204, 74.3587], zoom_start=12)

    folium.Marker(location=[31.5047, 74.3315], popup='Default popup Marker1',
                  tooltip='Click here to see Popup').add_to(m)
    folium.Marker(location=[31.511996, 74.343018], popup='Default popup Marker1',
                  tooltip='Click here to see Popup').add_to(m)

    print('mmm', m)
    m = m._repr_html_()
    context = {
        'map': m
    }

    return render(request, 'shopkeeper/dukandar/google_map.html', context)


@login_required(login_url='shopkeeper:admin_login')
def parent_sub_ajax_data(request):
    parentID = json.loads(str(request.POST.get('parentID')))
    parent_sub_list = SubCategory.objects.filter(parent=parentID, is_active=True)
    sub_list = []
    for sub in parent_sub_list:
        sub_list.append({
            'id': sub.id,
            'name': sub.name
        })
    context = {
        'parent_sub_list': json.dumps(sub_list)
    }

    return JsonResponse(context, status=200)


@login_required(login_url='shopkeeper:admin_login')
def admin_logout(request):
    logout(request)
    return redirect('shopkeeper:admin_login')


@login_required(login_url='shopkeeper:admin_login')
def giftList(request):
    gift_list = GiftSpin.objects.all()
    context = {
        'gift_list': gift_list,
    }
    return render(request, 'shopkeeper/gift/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def giftSetup(request):
    if request.POST:
        gift_ID = request.POST.get('id', None)
        if gift_ID:
            gift_obj = GiftSpin.objects.get(id=gift_ID)
            gift_obj.name = request.POST.get('name', gift_obj.name)
            gift_obj.quantity = request.POST.get('quantity', gift_obj.quantity)
            gift_obj.amount = request.POST.get('amount', gift_obj.amount)
            gift_obj.save()
            messages.success(request, 'Gift Updated  Successfully ')
            return redirect('shopkeeper:gift_List')

        else:
            form = GiftSpinForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Gift Added  Successfully ')
                return redirect('shopkeeper:gift_List')

            else:
                messages.error(request, 'Invalid Data')
                return redirect('shopkeeper:gift_Setup')

    else:
        return render(request, 'shopkeeper/gift/setup.html')


def giftDetails(request, pk):
    try:
        gift_obj = GiftSpin.objects.get(id=pk)

        context = {
            'gift_obj': gift_obj,
            'id': pk
        }
        return render(request, 'shopkeeper/gift/setup.html', context)
    except GiftSpin.DoesNotExist:
        messages.error(request, 'Record Not Found')
        return redirect('shopkeeper:gift_Setup')


def giftDelete(request, pk):
    gift_obj = GiftSpin.objects.get(id=pk)
    gift_obj.delete()
    messages.error(request, 'Record Deleted')
    return redirect('shopkeeper:gift_List')


@login_required(login_url='shopkeeper:admin_login')
def ordersHistoryList(request):
    orders_list = OrderHistory.objects.all()
    shopkeeper = None
    customer = None
    for order in orders_list:
        shopkeeper = order.order.shopkeeper
        customer = order.order.customer
    print('shopkeeper', customer)
    context = {
        'orders_list': orders_list,
        'shopkeeper': shopkeeper,
        'customer': customer
    }
    return render(request, 'shopkeeper/order/orderhistorylist.html', context)


@login_required(login_url='shopkeeper:admin_login')
def ordersHistoryDetails(request, pk):
    if request.POST:
        pdf = request.POST.get('PDF_BTN', None)
        print('PDF_BTN', pdf)
        if pdf:
            orders_obj = OrderHistory.objects.filter(id=pdf)

            orders_obj = OrderHistory.objects.get(id=pdf)
            shopkeeper_obj = orders_obj.shopkeeper or None
            customer_obj = orders_obj.customer or None
            product_orders = ProductOrderHistory.objects.filter(order_id=pk)
            # win_gift=WinSpin.objects.filter(shopkeeper_id=shopkeeper_obj.id)

            context = {
                'order_id': orders_obj.id,
                'products': product_orders,
                'dukandar': orders_obj.shopkeeper,
                'customer': orders_obj.customer,
                'order_date': orders_obj.order_date,
                'amount': orders_obj.total_amount,
                'discount': orders_obj.discount,
                'order_upto': orders_obj.order_upto,
                'shopkeeper_obj': shopkeeper_obj,
                'customer_obj': customer_obj,
                # 'win_gift_list':win_gift,

                'status': orders_obj.status,
            }

            pdf = render_to_pdf('shopkeeper/pdf.html', context)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="dukandarOrder#' + str(orders_obj.id) + '".pdf"'
            return response

        else:
            orders_obj = OrderHistory.objects.get(id=pk)
            orders_obj.status = request.POST['status']
            orders_obj.save()
            messages.success(request, 'Order Status Successfully')
            return redirect('shopkeeper:orders_list')
    else:

        orders_obj = OrderHistory.objects.get(id=pk)

        product_orders =ProductOrder.objects.filter(order=orders_obj.order.id)
     
        shopkeeper_id= orders_obj.order.shopkeeper or None
        customer_id= orders_obj.order.customer or None
        datalist=[]

        for prod in product_orders:
           
            datalist.append({
                'order_id': orders_obj.id,
                'p_quantity': prod.quantity,
                'p_name': prod.product.name,
                'p_price': prod.price,
                'sub_total': prod.sub_total,
                'dukandar': orders_obj.order.shopkeeper,
                # 'customer':orders_obj.customer,
                'order_update': orders_obj.created_at,

                'shopkeeper_id': shopkeeper_id,
                'customer_id': customer_id,

            })
        print('datalist', datalist)
        context = {
            'datalist': datalist,
            'order_id': orders_obj.id,
            # 'products': product_orders,
            # 'dukandar': orders_obj.order.shopkeeper,
            # # 'customer':orders_obj.customer,
            # 'order_date': orders_obj.created_at,
            'amount': orders_obj.order.total_amount,
            'discount': orders_obj.order.discount,
            'shopkeeper_id': shopkeeper_id,
            'customer_id': customer_id,
            #
            #
            'status': orders_obj.status,

        }

        return render(request, 'shopkeeper/order/orderhistorydetail.html', context)


@login_required(login_url='shopkeeper:admin_login')
def complaintsList(request):
    complaint_list = Complaints.objects.all()

    context = {
        'complaint_list': complaint_list,

    }
    return render(request, 'shopkeeper/complaints/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def complaintsDetail(request, pk):
    comp_obj = Complaints.objects.get(id=pk)

    context = {
        'comp_obj': comp_obj,

    }
    return render(request, 'shopkeeper/complaints/detail.html', context)


@login_required(login_url='shopkeeper:admin_login')
def complaintsDelete(request, pk):
    comp_obj = Complaints.objects.get(id=pk)
    comp_obj.delete()
    messages.error(request, 'Record Deleted')
    return redirect('shopkeeper:complaints_list')


@login_required(login_url='shopkeeper:admin_login')
def notificationList(request):
    notification_list = Notification.objects.all()
    context = {
        'notification_list': notification_list,
    }
    return render(request, 'shopkeeper/notification/list.html', context)


@login_required(login_url='shopkeeper:admin_login')
def notificationSetup(request):
    if request.POST:
        noti_ID = request.POST.get('id', None)
        if noti_ID:
            noti_obj = Notification.objects.get(id=noti_ID)
            noti_obj.name = request.POST.get('name', noti_obj.name)
            noti_obj.save()
            messages.success(request, 'Notification Updated  Successfully ')
            return redirect('shopkeeper:notification_List')

        else:
            print('request.POST', request.POST)
            form = NotificationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Notification Added  Successfully ')
                return redirect('shopkeeper:notification_List')

            else:
                messages.error(request, 'Invalid Data')
                return redirect('shopkeeper:notification_Setup')

    else:
        return render(request, 'shopkeeper/notification/setup.html')


def notificationDetail(request, pk):
    try:
        noti_obj = Notification.objects.get(id=pk)

        context = {
            'noti_obj': noti_obj,
            'id': pk
        }
        return render(request, 'shopkeeper/notification/setup.html', context)
    except GiftSpin.DoesNotExist:
        messages.error(request, 'Record Not Found')
        return redirect('shopkeeper:notification_Setup')


def notificationDelete(request, pk):
    noti_obj = Notification.objects.get(id=pk)
    noti_obj.delete()
    messages.error(request, 'Record Deleted')
    return redirect('shopkeeper:notification_List')


# def password_reset_request(request):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = User.objects.filter(Q(email=data))
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
# 					email_template_name = "main/password/password_reset_email.txt"
# 					c = {
# 					"email":user.email,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return redirect ("/password_reset/done/")
# 	password_reset_form = PasswordResetForm()
# 	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})

def privacy_policy(request):
    return render(request, 'shopkeeper/privacy.html')