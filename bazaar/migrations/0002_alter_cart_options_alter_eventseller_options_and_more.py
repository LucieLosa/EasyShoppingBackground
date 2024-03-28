# Generated by Django 4.2 on 2023-09-13 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bazaar', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['event', 'name']},
        ),
        migrations.AlterModelOptions(
            name='eventseller',
            options={'ordering': ['event', 'seller']},
        ),
        migrations.AlterModelOptions(
            name='eventuser',
            options={'ordering': ['event', 'user']},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['cart', 'event_seller', 'price']},
        ),
        migrations.AlterModelOptions(
            name='seller',
            options={'ordering': ['nickname']},
        ),
        migrations.RenameField(
            model_name='eventseller',
            old_name='is_fees',
            new_name='is_no_fees',
        ),
        migrations.RenameField(
            model_name='seller',
            old_name='is_fees_default',
            new_name='is_no_fees_default',
        ),
        migrations.AlterField(
            model_name='item',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaar.cart', verbose_name='Cart'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='nickname',
            field=models.CharField(max_length=128, unique=True, verbose_name='Unique nickname - quick find'),
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('name', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='eventseller',
            unique_together={('event', 'seller')},
        ),
        migrations.AlterUniqueTogether(
            name='eventuser',
            unique_together={('event', 'user')},
        ),
    ]