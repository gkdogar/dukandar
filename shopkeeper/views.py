from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from bootstrap_modal_forms.generic import BSModalCreateView
# Create your views here.
from .forms import *
from .models.models import *
from django.views import View
from django.views.generic import ListView
from django.contrib import messages


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
        object_list = Employee.objects.all()

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
class ParentCategorySetupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'shopkeeper/product/parent_category_setup.html')


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
