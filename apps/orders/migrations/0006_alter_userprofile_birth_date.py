# Generated by Django 4.2.6 on 2023-10-10 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_userprofile_groups_userprofile_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(blank=True),
        ),
    ]