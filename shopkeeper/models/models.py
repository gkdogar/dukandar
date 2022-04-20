from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import timezone
from shopkeeper.models.customManager import *
from django.utils.translation import gettext_lazy as _
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from time import gmtime
from time import strftime
from django.core.mail import EmailMessage
from django.template.loader import get_template
from decouple import config
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.template.loader import render_to_string
EMAIL_HOST_USER = config('EMAIL_HOST_USER')



USER_CHOICES = (

    ('SUPER_ADMIN', 'Super Admin'),
    ('STAFF', 'Staff'),
    ('SHOPKEEPER', 'Shopkeeper'),
    ('CUSTOMER', 'Customer'),
)

ORDER_CHOICES = (('CANCELLED', 'cancelled'), ('DELIVERED', 'delivered '),
                 ('PROCESSING', 'processing'),
                 )
CATEGORY_FOR_CHOICES = (('BRAND', 'For Brand'), ('RETAIL', 'For Retail'),
                        ('WSALE', 'For Whole Sale'),
                        ('CULTURE', 'For Culture'), ('AUTO', 'For Auto'))

SHOPKEEPER_CHOICES = (

    ('RETAIL', 'Retail'),
    ('WSALE', 'Wholesale'),

)


class User(AbstractUser):
    city = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=250, null=True)
    phone_no = models.CharField(max_length=250, null=True)
    user_type = models.CharField(max_length=16,
                                 choices=USER_CHOICES,
                                 default="CUSTOMER")

    block = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(_('email address'), unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def token(self):
        token = jwt.encode({'email': self.email, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY,
                           algorithm='HS256')
        return token

    objects = UserManager()

    def __str__(self):
        return self.email


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE, null=False)
    target_assign = models.IntegerField(default=0, null=True, blank=True)
    target_achieved = models.IntegerField(default=0, null=True, blank=True)
    area_designated = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=datetime.now())

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)

    def __init__(self, name, email, house_id, password, *args, **kwargs):
        super(models.Model, self).__init__(self, *args, **kwargs)
        self.name = name
        self.email = email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.updated_at:
            target_add_date = self.updated_at
            current_date = datetime.today()
            # created_at__gt=datetime.today() + timedelta(days=1)
            if target_add_date.date() < current_date.date():
                emp_histroy = EmployeeHistry.objects.create(employee=self, daily_target_assign=self.target_assign,
                                                            daily_achieved=self.target_achieved)
                emp_histroy.save()
                self.target_achieved = 0
                self.save()
        # add your own logic


class EmployeeHistry(models.Model):
    employee = models.ForeignKey(Employee, related_name='employee', on_delete=models.CASCADE)
    daily_target_assign = models.CharField(max_length=10, null=True)
    daily_achieved = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return str(self.employee.user.first_name + ' ' + self.employee.user.last_name)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)


class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    shopkeeper_type = models.CharField(choices=SHOPKEEPER_CHOICES,
                                       max_length=7,
                                       default='RETAIL')
    shop_name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    latitude = models.CharField(max_length=50, null=False)
    longitude = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user.email)


class ParentCategory(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    meta_keywords = models.CharField(max_length=255, null=True)
    meta_description = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='product/category/parent')
    category_for = models.CharField(choices=CATEGORY_FOR_CHOICES,
                                    max_length=7,
                                    default='RETAIL')
    is_active = models.BooleanField(default=False)

    # commission = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name + " - " + self.category_for


class SubCategory(models.Model):
    parent = models.ForeignKey(ParentCategory,
                               on_delete=models.CASCADE,
                               null=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    meta_keywords = models.CharField(max_length=255, null=True)
    meta_description = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='product/category/sub')
    is_active = models.BooleanField(default=False)

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    # shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE)
    parent = models.ForeignKey(ParentCategory,
                               on_delete=models.CASCADE, related_name='ParentCategory',
                               null=True)
    sub_cat = models.ForeignKey(SubCategory,
                                on_delete=models.CASCADE,
                                null=True)
    name = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='product/category/sub')
    description = models.TextField()
    # sku = models.CharField(max_length=100, null=False,blank=True)
    quantity = models.IntegerField(default=0)
    r_price = models.FloatField(default=0.0)
    w_price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)

    # weight_unit = models.CharField(max_length=5, choices=WEIGHT_UNIT_SELECTION, default="KG")

    # category = models.ManyToManyField(ProductCategory)

    # parent_cat = models.CharField(max_length=100, null=True)
    # sub_cat = models.CharField(max_length=100, null=True)
    # product_cat = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper,
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True
                                   )
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)

    total_amount = models.BigIntegerField(default=0)
    order_upto = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    discount = models.IntegerField(default=0)
    status = models.CharField(choices=ORDER_CHOICES,
                              max_length=12,
                              default='PROCESSING')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.total_amount)


class ProductOrder(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              null=True)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=True)
    quantity = models.IntegerField(default=0)

    price = models.IntegerField(default=0)

    sub_total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderHistory(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True
                              )
    status = models.CharField(choices=ORDER_CHOICES,
                            max_length=12,
                            default='PROCESSING')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order)


class ProductOrderHistory(models.Model):
    order = models.ForeignKey(OrderHistory,
                              on_delete=models.CASCADE,
                              null=True)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=True)
    quantity = models.IntegerField(default=0)

    price = models.IntegerField(default=0)

    sub_total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)


class Discount(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='discount_on_product',
                                )
    shopkeeper = models.ForeignKey(Shopkeeper,
                                   on_delete=models.CASCADE,
                                   null=True)
    discount = models.IntegerField(default=0)
    start_from = models.DateTimeField(auto_now=True)
    end_from = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.discount


class Wallet(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper,
                                   on_delete=models.CASCADE,
                                   null=True)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              null=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.amount)


class Complaints(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper,
                                   on_delete=models.CASCADE,
                                   null=True, blank=True)
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)
    # order = models.ForeignKey(Order,
    #                           on_delete=models.CASCADE,
    #                           null=True, blank=True)
    message = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.message


class Spines(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper,
                                   on_delete=models.CASCADE,
                                   null=True)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              null=True)
    amount = models.IntegerField(default=0)

    spine_no = models.IntegerField(default=0)

    def __str__(self):
        return str(self.spine_no)


class GiftSpin(models.Model):
    name = models.CharField(max_length=250, null=True)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class WinSpin(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper,
                                   on_delete=models.CASCADE,
                                   null=True)
    giftSpin = models.ForeignKey(GiftSpin,
                                 on_delete=models.CASCADE,
                                 null=True)


class Notification(models.Model):
    name = models.CharField(max_length=250, null=True)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    # email_plaintext_message = "{}?token={}".format(reverse("{% url 'password_reset'%}"), reset_password_token.key)
    print('sendsssssser',sender)
    # email_plaintext_message = "{}?token={}".format(reverse('password_reset'), reset_password_token.key)
    # msg_html = render_to_string('shopkeeper/email/password_reset.html')
    # send_mail(
    #     # title:
    #     "Password Reset for {title}".format(title="Some website title"),
    #     # message:
    #     msg_html,
      
    #     # from:
    #    '101620014umt@gmail.com',
    #     # to:
    #     [reset_password_token.user.email]
    # )
    message = get_template("shopkeeper/email/password_reset.html").render({'token':reset_password_token.key})
    mail = EmailMessage(
        subject="Password Reset Email",
        body=message,
        from_email= '101620014umt@gmail.com',
        to= [reset_password_token.user.email],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=False)

    # subject = "Password Reset Requested"
	# 				email_template_name = "main/password/password_reset_email.txt"
	# 				c = {
	# 				"email":user.email,
	# 				'domain':'127.0.0.1:8000',
	# 				'site_name': 'Website',
	# 				"uid": urlsafe_base64_encode(force_bytes(user.pk)),
	# 				"user": user,
	# 				'token': default_token_generator.make_token(user),
	# 				'protocol': 'http',
	# 				}
	# 				email = render_to_string(email_template_name, c)
	# 				try:
	# 					send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
	# 				except BadHeaderError:
	# 					return HttpResponse('Invalid header found.')
