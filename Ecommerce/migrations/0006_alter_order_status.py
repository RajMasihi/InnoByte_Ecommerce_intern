# Generated by Django 4.2.16 on 2024-10-30 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0005_alter_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('paid', 'paid'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('canceled', 'canceled')], default='pending', max_length=25),
        ),
    ]
