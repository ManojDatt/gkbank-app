# Generated by Django 3.1 on 2020-08-14 07:29

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_model_changes.changes
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Last name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Account active')),
                ('is_staff', models.BooleanField(default=True, help_text='Designates whether the user can log into this portal.', verbose_name='staff status')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group', verbose_name='Role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': '  Users',
            },
            bases=(django_model_changes.changes.ChangesMixin, models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalUsers',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(db_index=True, max_length=100, verbose_name='Username')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='Email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Last name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Account active')),
                ('is_staff', models.BooleanField(default=True, help_text='Designates whether the user can log into this portal.', verbose_name='staff status')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Updated at')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auth.group', verbose_name='Role')),
            ],
            options={
                'verbose_name': 'historical User',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBankAccounts',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('account_number', models.CharField(db_index=True, max_length=100, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(12)], verbose_name='Label')),
                ('balance', models.FloatField(default=0, verbose_name='Balance')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Updated At')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('customer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical  Account',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='BankAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(12)], verbose_name='Label')),
                ('balance', models.FloatField(default=0, verbose_name='Balance')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
            options={
                'verbose_name': ' Account',
                'verbose_name_plural': ' Accounts',
            },
        ),
    ]
