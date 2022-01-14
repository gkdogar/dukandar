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

def index(request):
    return render(request, 'shopkeeper/admin/dashboard.html')


class EmployeeListView(ListView):
    paginate_by = 100
    template_name = 'shopkeeper/customer/list.html'

    def get_queryset(self):
        # user_obj=User.objects.filter(is_staff=True )
        # for user in user_obj:
        #    print('user',user)
        #    object_list= Employee.objects.filter(user=user.id)
        #    print('object_list',object_list)
        object_list = User.objects.filter(user_type='STAFF')

        return object_list


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
            print('req', request.FILES)
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
