# Generated by Django 4.2 on 2023-09-13 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=128, verbose_name='Name')),
                ('number', models.PositiveSmallIntegerField(verbose_name='Number')),
                ('x_created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('x_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Closed')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('fee_value_default', models.PositiveSmallIntegerField(default=0, verbose_name='Static fee value default')),
                ('fee_value_percentage', models.PositiveSmallIntegerField(default=0, verbose_name='Percentage fee value default')),
                ('x_created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('x_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='EventSeller',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_fees', models.BooleanField(default=False)),
                ('total_sold_items', models.PositiveSmallIntegerField(default=0)),
                ('total_sales_amount', models.PositiveSmallIntegerField(default=0)),
                ('total_fees', models.PositiveSmallIntegerField(default=0)),
                ('x_created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('x_modified', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaar.event')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=128, verbose_name='Unique nickname - quick find')),
                ('name', models.CharField(blank=True, max_length=128, verbose_name='Name')),
                ('email', models.CharField(blank=True, max_length=128, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=128, verbose_name='Phone')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('default_number', models.PositiveSmallIntegerField(blank=True, verbose_name='Seller number (default setting)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_fees_default', models.BooleanField(default=False, verbose_name='No fees (default setting)')),
                ('x_created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('x_modified', models.DateTimeField(auto_now=True)),
                ('x_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('size', models.CharField(max_length=32, verbose_name='Size')),
                ('price', models.PositiveSmallIntegerField(default=0, verbose_name='Price')),
                ('x_created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('x_modified', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bazaar.cart', verbose_name='Cart')),
                ('event_seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bazaar.eventseller')),
                ('x_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventUser',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('x_created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('x_modified', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaar.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('x_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='x_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='eventseller',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaar.seller'),
        ),
        migrations.AddField(
            model_name='eventseller',
            name='x_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='sellers',
            field=models.ManyToManyField(through='bazaar.EventSeller', to='bazaar.seller'),
        ),
        migrations.AddField(
            model_name='event',
            name='x_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='events_x_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bazaar.event', verbose_name='bazaar'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='carts_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='x_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='carts_x_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
