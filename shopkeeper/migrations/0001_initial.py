# Generated by Django 4.0.1 on 2022-02-05 19:14

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('address', models.CharField(max_length=250, null=True)),
                ('user_type', models.CharField(choices=[('SUPER_ADMIN', 'Super Admin'), ('STAFF', 'Staff'), ('SHOPKEEPER', 'Shopkeeper'), ('CUSTOMER', 'Customer')], default='CUSTOMER', max_length=16)),
                ('block', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_assign', models.CharField(max_length=10, null=True)),
                ('target_achieved', models.CharField(max_length=10, null=True)),
                ('area_designated', models.CharField(blank=True, max_length=250, null=True)),
                ('phone_no', models.CharField(max_length=20, null=True)),
                ('description', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField(default=0)),
                ('order_upto', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('CANCELLED', 'cancelled'), ('DELIVERED', 'delivered '), ('PROCESSING', 'processing')], default='PROCESSING', max_length=12)),
                ('cutomer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ParentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('meta_keywords', models.CharField(max_length=255, null=True)),
                ('meta_description', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(upload_to='product/category/parent')),
                ('category_for', models.CharField(choices=[('BRAND', 'For Brand'), ('RETAIL', 'For Retail'), ('WSALE', 'For Whole Sale'), ('CULTURE', 'For Culture'), ('AUTO', 'For Auto')], default='RETAIL', max_length=7)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Shopkeeper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=255)),
                ('phone_no', models.CharField(max_length=20)),
                ('description', models.TextField(null=True)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.employee')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.order')),
                ('shopkeeper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.shopkeeper')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('meta_keywords', models.CharField(max_length=255, null=True)),
                ('meta_description', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(upload_to='product/category/sub')),
                ('is_active', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.parentcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Spines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('spine_no', models.IntegerField(default=0)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.order')),
                ('shopkeeper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.shopkeeper')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='product/category/sub')),
                ('description', models.TextField()),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0.0)),
                ('discount', models.FloatField(default=0.0)),
                ('is_active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ParentCategory', to='shopkeeper.parentcategory')),
                ('sub_cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField(default=0)),
                ('order_upto', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('CANCELLED', 'cancelled'), ('DELIVERED', 'delivered '), ('PROCESSING', 'processing')], default='PROCESSING', max_length=12)),
                ('cutomer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.customer')),
                ('previouse_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.product')),
                ('shopkeeper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.shopkeeper')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='shopkeeper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.shopkeeper'),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(default=0)),
                ('start_from', models.DateTimeField(auto_now=True)),
                ('end_from', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount_on_product', to='shopkeeper.product')),
                ('shopkeeper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.shopkeeper')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.employee')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.order')),
                ('shopkeeper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.shopkeeper')),
            ],
        ),
    ]
