# Generated by Django 4.1.5 on 2024-05-19 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('no_of_installments', models.IntegerField(default=0)),
                ('started_on', models.DateField()),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open', max_length=20)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Financial Product',
                'verbose_name_plural': 'Financial Products',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('Personal', 'Personal'), ('Loan', 'Loan'), ('Food', 'Food'), ('Shopping', 'Shopping')], default='Personal', max_length=50)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('beneficiary', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('mode', models.CharField(choices=[('CreditCard', 'CreditCard'), ('Online', 'Online'), ('Cash', 'Cash')], max_length=10, null=True)),
                ('mode_detail', models.CharField(max_length=10, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
                ('source', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.financialproduct')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(blank=True, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('complete_by_date', models.DateField()),
                ('description', models.TextField(blank=True, max_length=500)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('completed_on', models.DateField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.AddField(
            model_name='financialproduct',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
    ]
