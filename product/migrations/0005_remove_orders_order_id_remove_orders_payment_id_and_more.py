# Generated by Django 4.2.6 on 2023-10-27 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_orderitems_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='payment_signature',
        ),
    ]
