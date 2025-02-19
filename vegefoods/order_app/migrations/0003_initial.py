# Generated by Django 5.1 on 2024-09-02 03:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address_app', '0002_alter_address_address_type'),
        ('order_app', '0002_remove_orderitem_order_remove_orderitem_product_and_more'),
        ('product_apps', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=20, unique=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Return', 'Return')], default='Pending', max_length=20)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_type', models.CharField(choices=[('COD', 'Cash on Delivery'), ('RazorPay', 'Razor Pay'), ('UPI', 'UPI')], max_length=20)),
                ('estimated_delivery_date', models.DateField(blank=True, null=True)),
                ('coupon_code', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address_app.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order_app.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_apps.product')),
            ],
        ),
    ]
