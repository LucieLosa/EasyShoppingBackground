# Generated by Django 4.2 on 2023-10-21 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0005_alter_cart_options_alter_event_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Velikost'),
        ),
    ]