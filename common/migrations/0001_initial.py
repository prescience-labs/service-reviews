# Generated by Django 2.2.5 on 2019-09-13 22:20

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vendor_product_id', models.CharField(help_text='The vendor-specific product ID', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('integrations_type', models.CharField(blank=True, help_text='Set by the integrations service to uniquely identify a vendor', max_length=1000, null=True)),
                ('integrations_id', models.CharField(blank=True, help_text='Set by the integrations service to uniquely identify a vendor', max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('integrations_type', 'integrations_id')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer_email', models.CharField(blank=True, max_length=500, null=True)),
                ('customer_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('products', models.ManyToManyField(to='common.Product')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='vendors',
            field=models.ManyToManyField(through='common.Inventory', to='common.Vendor'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Product'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Vendor'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(blank=True, help_text='The review rating, if it was included', null=True)),
                ('rating_max', models.PositiveSmallIntegerField(blank=True, help_text='The max possible review rating, if it was included', null=True)),
                ('analytics_id', models.UUIDField(blank=True, help_text='The document id from the <a href="https://data-intel-documents-dev.herokuapp.com/v1">Documents Service</a>', null=True)),
                ('sentiment_analysis', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='The sentiment analysis from the document service', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, help_text='The product this review is about', null=True, on_delete=django.db.models.deletion.CASCADE, to='common.Product')),
                ('transaction', models.ForeignKey(blank=True, help_text='The transaction associated with this review', null=True, on_delete=django.db.models.deletion.CASCADE, to='common.Transaction')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Vendor')),
            ],
            options={
                'unique_together': {('transaction', 'product')},
            },
        ),
    ]
