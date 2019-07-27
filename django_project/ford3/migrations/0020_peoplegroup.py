# Generated by Django 2.1.9 on 2019-07-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ford3', '0019_auto_20190719_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeopleGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, help_text='A group of people.', max_length=255, null=True, unique=True)),
            ],
        ),
    ]
