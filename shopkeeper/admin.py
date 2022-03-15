from django.contrib import admin

# Register your models here.
from .models.models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from import_export.admin import ImportExportModelAdmin, post_export, post_import

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    fieldsets = ((None, {
        'fields':
        ('first_name', 'last_name', 'email','city', 'phone_no','password', 'groups',
        'address','user_type')
    }), )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'password1', 'password2'),
    }), )
    list_display = ('email', 'first_name', 'last_name', 'user_type')
    search_fields = ('email', 'first_name', 'last_name', 'user_type')
    ordering = ('email', )

admin.site.register(GiftSpin)
admin.site.register(WinSpin)
admin.site.register(ProductOrder)
admin.site.register(Shopkeeper)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(ParentCategory,ImportExportModelAdmin)
admin.site.register(SubCategory,ImportExportModelAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderHistory)
admin.site.register(Discount)
admin.site.register(Spines)
admin.site.register(Wallet)
admin.site.register(Complaints)
admin.site.register(ProductOrderHistory)


@admin.register(EmployeeHistry)
class EmployeeHistryAdmin(admin.ModelAdmin):
  
    list_display = ('daily_target_assign', 'daily_achieved', 'created_at')
    search_fields = ( 'daily_target_assign', 'daily_achieved', 'created_at')
   