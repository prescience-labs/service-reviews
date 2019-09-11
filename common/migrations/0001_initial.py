# Generated by Django 2.2.5 on 2019-09-11 13:27

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('source', models.CharField(help_text='The source of the review (e.g. Google, Shopify, Amazon)', max_length=255)),
                ('rating', models.PositiveSmallIntegerField(blank=True, help_text='The review rating, if it was included', null=True)),
                ('rating_max', models.PositiveSmallIntegerField(blank=True, help_text='The max possible review rating, if it was included', null=True)),
                ('analytics_id', models.UUIDField(blank=True, help_text='The document id from the documents service (https://data-intel-documents-dev.herokuapp.com/v1)', null=True)),
                ('sentiment_analysis', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='The sentiment analysis from the document service', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
