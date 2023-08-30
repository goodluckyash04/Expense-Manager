# Generated by Django 4.2.2 on 2023-08-30 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emi',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='status',
            field=models.CharField(default='Open', max_length=20),
        ),
        migrations.AlterField(
            model_name='emi',
            name='paid_on',
            field=models.DateTimeField(),
        ),
    ]
