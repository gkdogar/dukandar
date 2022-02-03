from django.db import models
from django.contrib.auth.models import AbstractUser

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



class User(AbstractUser):
    address = models.CharField(max_length=250, null=True)
    user_type = models.CharField(max_length=16,
                                 choices=USER_CHOICES,
                                 default="CUSTOMER")

    block = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Employee(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, null=False)
    target_assign = models.CharField(max_length=10, null=True)
    target_achieved = models.CharField(max_length=10, null=True)
    area_designated = models.CharField(max_length=250, null=True)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_no = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)

class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False)
    shop_name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    description = models.TextField(null=True)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.user.username

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
                               on_delete=models.CASCADE,
                               null=True)
    sub_cat = models.ForeignKey(SubCategory,
                                on_delete=models.CASCADE,
                                null=True)
    name = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='product/category/sub')
    description = models.TextField()
    # sku = models.CharField(max_length=100, null=False,blank=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
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
    product = models.ForeignKey(Product,
                               on_delete=models.CASCADE,
                               null=True)
    shopkeeper = models.ForeignKey(Shopkeeper,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    customer = models.ForeignKey(Customer,
                                   on_delete=models.CASCADE,
                                   null=True,blank=True)
    order_date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    order_upto =  models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    status=models.CharField(choices=ORDER_CHOICES,
                                    max_length=12,
                                    default='PROCESSING')

    def __str__(self):
        return str(self.order_date)

class OrderHistory(models.Model):

    previouse_order = models.ForeignKey(Order,
                               on_delete=models.CASCADE,
                             )
    product = models.ForeignKey(Product,
                               on_delete=models.CASCADE,
                               null=True)
    shopkeeper = models.ForeignKey(Shopkeeper,
                               on_delete=models.CASCADE,
                               null=True)
    cutomer = models.ForeignKey(Customer,
                                   on_delete=models.CASCADE,
                                   null=True)
    order_date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    order_upto =  models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    status=models.CharField(choices=ORDER_CHOICES,
                                    max_length=12,
                                    default='PROCESSING')

class Discount(models.Model):
    product = models.ForeignKey(Product,
                               on_delete=models.CASCADE,
                               null=True,
                               related_name = 'discount_on_product',
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
        return self.amount

class Complaint(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper,
                                on_delete=models.CASCADE,
                                null=True)
    employee = models.ForeignKey(Employee,
                                   on_delete=models.CASCADE,
                                   null=True)
    order = models.ForeignKey(Order,
                                on_delete=models.CASCADE,
                                null=True)
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
        return self.spine_no

