# Generated by Django 4.2.6 on 2023-10-10 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_userprofile_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=150),
        ),
    ]
