from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models.models import *
from bootstrap_modal_forms.forms import BSModalModelForm

class EmployeeModelForm(BSModalModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class ExtendUserCreationForm(UserCreationForm):
    email =forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model =User
        fields =('email','first_name','last_name')

    def save(self, commit=True):
        user =super().save(commit=False)
        user.email =self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class ShopkeeperForm(ModelForm):

    class Meta:
        model =Shopkeeper
        fields=('emp_id', 'shop_name','description')

class ParentCategoryForm(ModelForm):

    class Meta:
        model =ParentCategory
        fields='__all__'

class SubCategoryForm(ModelForm):

    class Meta:
        model =SubCategory
        fields='__all__'

class ProductForm(ModelForm):

    class Meta:
        model =Product
        fields='__all__'

class GiftSpinForm(ModelForm):
    class Meta:
        model =GiftSpin
        fields=['name', 'quantity', 'amount']
