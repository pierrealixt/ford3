# Generated by Django 2.1.7 on 2019-05-28 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ford3', '0005_user_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ford3.Province'),
        ),
    ]