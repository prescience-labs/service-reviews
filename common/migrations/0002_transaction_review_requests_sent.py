# Generated by Django 2.2.5 on 2019-09-18 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='review_requests_sent',
            field=models.PositiveSmallIntegerField(default=0, help_text="The number of review requests we've sent to the customer regarding this transaction"),
        ),
    ]