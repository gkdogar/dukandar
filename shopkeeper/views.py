from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from bootstrap_modal_forms.generic import BSModalCreateView
# Create your views here.
from .forms import *
from .models.models import *
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
import folium
import re
from django.http import JsonResponse
import json


def index(request):
    return render(request, 'shopkeeper/base/base.html')




class EmployeeListView(ListView):
    paginate_by = 100
    template_name = 'shopkeeper/customer/list.html'

    def get_queryset(self):
        # user_obj=User.objects.filter(is_staff=True )
        # for user in user_obj:
        #    print('user',user)
        #    object_list= Employee.objects.filter(user=user.id)
        #    print('object_list',object_list)
        object_list = Employee.objects.all()

        return object_list

def employeeSetup(request):
    if request.POST:
        print('user Exist',request.POST)
        username= request.POST.get('username')
        password= request.POST.get('password')
        password1= request.POST.get('password1')
        check_user = User.objects.filter(username=username)
        if check_user.count() == 1:
            messages.error(request, 'UserName Already Existed')
            return redirect('employee_setup')
        if password != password1:
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pat = re.compile(reg)               
            mat = re.search(pat, password)
            if mat:
                print("Password is valid.")
            else:
                messages.error(request, 'Password Must contains one Capital and One Speceial Char')
                return redirect('employee_setup')
            messages.error(request, 'Password must be matched!')
            return redirect('employee_setup')
        user= User.objects.create_user(username=username,password=password)
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.email=request.POST.get('email')
        user.address=request.POST.get('address')
        user.user_type='STAFF'
        user.save()
        employee=Employee.objects.create(user=user, target_assign=request.POST.get('target_assign'), target_achieved=request.POST.get('target_achieved'), area_designated=request.POST.get('area_designated'), description =request.POST.get('description'),is_active =request.POST.get('is_active'))
        employee.save()
        messages.success(request, 'Record Created Successfully')
        return redirect('employee_list')
    else:
 
        return render(request, 'shopkeeper/employee/setup.html')

def employeeList(request): 
    employee_list =Employee.objects.all()
    context={
        'employee_list':employee_list
    }
    return render(request, 'shopkeeper/employee/list.html',context)

def employeeUpdate(request,pk):
    context={
        'emp_id':1
    }
    return render(request, 'shopkeeper/employee/setup.html',context)

def employeeDelete(request):
    return render(request, 'shopkeeper/employee/setup.html')

def dukandarList(request):
    dukandars_list=Shopkeeper.objects.all()
    context ={
        'dukandars_list':dukandars_list
    }
    return render(request, 'shopkeeper/dukandar/list.html',context)


def dukandarSetup(request):
    return render(request, 'shopkeeper/dukandar/setup.html')
def dukandarUpdate(request, pk):

    return render(request, 'shopkeeper/dukandar/setup.html')
def dukandarDelete(request):
    return render(request, 'shopkeeper/dukandar/setup.html')

def customerSetup(request):
    return render(request, 'shopkeeper/customer/setup.html')
def customerList(request):
    return render(request, 'shopkeeper/customer/list.html')
def customerDetail(request):
    return render(request, 'shopkeeper/customer/setup.html')
def customerDelete(request):
    return render(request, 'shopkeeper/customer/setup.html')

# @method_decorator(login_required, name='dispatch')
class EmployeeSetupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'shopkeeper/customer/setup.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')

        check_user = User.objects.filter(username=username)
        if check_user:
            # messages.error(request, 'Employee Already Existed')
            messages.add_message(request, messages.ERROR, 'Employee already existed')
            return render(request, 'shopkeeper/customer/setup.html')

        else:
            user = User.objects.create_user(username, password)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.is_staff = True
            user.user_type = 'STAFF'
            user.save()
            employee = Employee.objects.create(user=user)
            employee.save()

        messages.success(request, 'Employee Record Created Successfully ')
        return redirect('employee_List')


# class CustomerSetupView(BSModalCreateView):
#     template_name = 'shopkeeper/customer/setup.html'
#     form_class = EmployeeModelForm
#     success_message = 'Success: Book was created.'
#     success_url = reverse_lazy('index')
def parent_category_list(request):
    parent_list=ParentCategory.objects.all()
    context={
        'parent_list':parent_list
    }
    return render(request, 'shopkeeper/product/parent_category_list.html', context)

def parent_category_detail(request, pk):

    parent_obj = ParentCategory.objects.get(id=pk)
    context = {
        'paren_id':parent_obj.id,
        'name': parent_obj.name,
        'description': parent_obj.description,
        'meta_keywords': parent_obj.meta_keywords,
        'meta_description': parent_obj.meta_description,
        'image': parent_obj.image,
        'category_for': parent_obj.category_for,
        'is_active': parent_obj.is_active,
    }
    return render(request, 'shopkeeper/product/parent_category_setup.html', context)

def parent_category_delete(request,pk):
    parent_delete = ParentCategory.objects.get(id=pk)
    parent_delete.delete()

    return redirect('parent_category_list')

class ParentCategorySetupView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'shopkeeper/product/parent_category_setup.html')

    def post(self, request, *args, **kwargs):

        paren_id =request.POST.get('paren_id') or None
        if paren_id:
            parent_obj = ParentCategory.objects.get(id=paren_id)
            img =parent_obj.image
            parent_obj.name=request.POST.get('name')
            parent_obj.description = request.POST.get('description')
            parent_obj.meta_keywords = request.POST.get('meta_keywords')
            parent_obj.meta_description = request.POST.get('meta_description')
            parent_obj.image=request.FILES.get('image') or img
            parent_obj.is_active=request.POST.get('is_active')or False
            parent_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            return redirect('parent_category_list')
        else:
            form = ParentCategoryForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Created Successfully')
                return redirect('parent_category_list')
            else:
                messages.error(request, 'Something Went Wrong')
                return redirect('parent_category_setup')


def sub_categoryList(request):
    sub_category_list=SubCategory.objects.all()
    context={
        'sub_category_list':sub_category_list
    }
    return render(request, 'shopkeeper/sub/list.html', context)

def sub_categorySetup(request):
    if request.POST:
        sub_id =request.POST.get('sub_id') or None
        if sub_id:
            sub_obj = SubCategory.objects.get(id=sub_id)
            img =sub_obj.image
            sub_obj.parent = ParentCategory.objects.get(id=request.POST.get('parent'))
            sub_obj.name=request.POST.get('name')
            sub_obj.description = request.POST.get('description')
            sub_obj.meta_keywords = request.POST.get('meta_keywords')
            sub_obj.meta_description = request.POST.get('meta_description')
            sub_obj.image=request.FILES.get('image') or img
            sub_obj.is_active=request.POST.get('is_active')or False
            sub_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            return redirect('parent_sub_category_list')

        else:
            form = SubCategoryForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Created Successfully')
                return redirect('parent_sub_category_list')
            else:
                messages.error(request, 'Something Went Wrong')
                return redirect('parent_sub_category_setup')
    else:
        parent_cat_list =ParentCategory.objects.filter(is_active=True)
        context ={
            'parent_cat_list':parent_cat_list
        }
        return render(request, 'shopkeeper/sub/setup.html',context)

def sub_categoryUpdate(request, pk):
    sub_obj = SubCategory.objects.get(id=pk)
    parent_cat_list =ParentCategory.objects.all()
    context = {
        'parent_cat_list':parent_cat_list,
        'sub_id':sub_obj.id,
        'parent_id':sub_obj.parent.id,
        'name': sub_obj.name,
        'description': sub_obj.description,
        'meta_keywords': sub_obj.meta_keywords,
        'meta_description': sub_obj.meta_description,
        'image': sub_obj.image,
        'is_active': sub_obj.is_active,
    }
    return render(request, 'shopkeeper/sub/setup.html', context)

def sub_categoryDelete(request, pk):
     sub_obj = SubCategory.objects.get(id=pk)
     sub_obj.delete()
     messages.success(request, 'Record Deleted Successfully')
     return redirect('parent_sub_category_list')

def productList(request):
    products_list =Product.objects.all()
    context={
        'products_list':products_list
    }
    return render(request, 'shopkeeper/product/list.html', context)


def productSetup(request):

    if request.POST:
        product_id =request.POST.get('product_id') or None
        if product_id:
            prod_obj = Product.objects.get(id=product_id)
            img =prod_obj.image
            prod_obj.parent = ParentCategory.objects.get(id=request.POST.get('parent'))
            prod_obj.sub_cat = SubCategory.objects.get(id=request.POST.get('sub_cat'))
            prod_obj.name=request.POST.get('name')
            prod_obj.description = request.POST.get('description')
            prod_obj.price = request.POST.get('price')
            prod_obj.quantity = request.POST.get('quantity')
            prod_obj.discount = request.POST.get('discount')
            prod_obj.image=request.FILES.get('image') or img
            prod_obj.is_active=request.POST.get('is_active')or False
            prod_obj.save()
            messages.add_message(request, messages.SUCCESS, 'Record Updated Successfully')
            return redirect('product_ist')
        else:
            form = ProductForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Created Successfully')
                return redirect('product_ist')
            else:
               
                messages.error(request, 'Something Went Wrong')
                return redirect('product_setup')

    else:
        parent_cat_list =ParentCategory.objects.filter(is_active=True)
        parent_sub_list=SubCategory.objects.filter(is_active=True)
        context={
            'parent_cat_list':parent_cat_list,
            'parent_sub_list':parent_sub_list
        }
        return render(request, 'shopkeeper/product/setup.html',context)


def productUpdate(request, pk):
    prod_obj = Product.objects.get(id=pk)
    parent_cat_list =ParentCategory.objects.filter(is_active=True)
    parent_sub_list=SubCategory.objects.filter(is_active=True)
    context = {
        'parent_cat_list':parent_cat_list,
        'parent_sub_list':parent_sub_list,
        'product_id':prod_obj.id,
        'parent_id':prod_obj.parent.id,
        'sub_cat_id':prod_obj.sub_cat.id,
        'name': prod_obj.name,
        'image': prod_obj.image,
        'description': prod_obj.description,
        'quantity': prod_obj.quantity,
        'price': prod_obj.price,
        'discount': prod_obj.discount,
        'is_active': prod_obj.is_active,
    }
    return render(request, 'shopkeeper/product/setup.html', context)

def productDelete(request):
    return render(request, 'shopkeeper/product/setup.html')

def ordersList(request):
    orders_list =Order.objects.all()
    context={
        'orders_list':orders_list
    }
    return render(request, 'shopkeeper/order/list.html',context)

def ordersDetails(request, pk):
    if request.POST:
        orders_obj =Order.objects.get(id=pk)
        orders_obj.status=request.POST['status']
        orders_obj.save()
        messages.success(request, 'Order Status Successfully')
        return redirect('orders_list')
    else:
        orders_obj =Order.objects.get(id=pk)
        context={
            'order_id':orders_obj.id,
            'product': orders_obj.product,
            'dukandar':orders_obj.shopkeeper,
            'customer':orders_obj.customer,
            'order_date': orders_obj.order_date,
            'amount':orders_obj.amount,
            'order_upto':orders_obj.order_upto,
            'quantity': orders_obj.quantity,
            'status':orders_obj.status,

        }
        return render(request, 'shopkeeper/order/detail.html',context)

def walletList(request):
    return render(request, 'shopkeeper/wallet/list.html')

def spinesList(request):
    return render(request, 'shopkeeper/spins/list.html')

def register(request):
    if request.method == 'POST':
        print('request post', request.POST)
        form = ExtendUserCreationForm(request.POST)
        shopkeeper_form = ShopkeeperForm(request.POST)
        if form.is_valid() and shopkeeper_form.is_valid():
            user = form.save()
            print('user >', user)
            user.user_type='SHOPKEEPER'
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
            return redirect('index')
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


def google_map(request):
    locationlist=[]
    # for point in range(0, len(locationlist)):
    #     folium.Marker(locationlist[point], popup=df_counters['Name'][point]).add_to(map)
    m=folium.Map(location=[31.5204, 74.3587], zoom_start=12)
    folium.Marker(location=[31.5047, 74.3315], popup='Default popup Marker1',
                  tooltip='Click here to see Popup').add_to(m)
    folium.Marker(location=[31.511996, 74.343018], popup='Default popup Marker1',
                  tooltip='Click here to see Popup').add_to(m)


    print('mmm',m)
    m = m._repr_html_()
    context={
        'map':m
    }

    return render(request, 'shopkeeper/admin/google_map.html', context)

def parent_sub_ajax_data(request):
    parentID= json.loads(str(request.POST.get('parentID')))
    parent_sub_list =SubCategory.objects.filter(parent=parentID, is_active=True)
    sub_list=[]
    for sub in parent_sub_list:
        sub_list.append({
            'id':sub.id,
            'name':sub.name
        })
    context={
           'parent_sub_list': json.dumps(sub_list)
    }

    return JsonResponse(context, status=200)