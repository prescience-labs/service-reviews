# Generated by Django 2.2.5 on 2019-09-19 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_transaction_review_requests_sent'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('vendor', 'vendor_product_id'), ('vendor', 'product')},
        ),
    ]