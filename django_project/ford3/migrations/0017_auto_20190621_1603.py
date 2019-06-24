# Generated by Django 2.1.9 on 2019-06-21 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ford3', '0016_provider_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='campus',
            name='completion_rate',
            field=models.PositiveIntegerField(blank=True, default=0, help_text="How much of the campus' details has been completed?", null=True),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='completion_rate',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='What has the completion rate for this qualifcation been?', null=True),
        ),
    ]
