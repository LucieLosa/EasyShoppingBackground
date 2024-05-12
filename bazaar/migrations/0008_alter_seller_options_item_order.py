# Generated by Django 4.2 on 2024-04-27 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0007_event_short_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seller',
            options={'ordering': ['default_identifier', 'nickname'], 'verbose_name': 'Prodejce', 'verbose_name_plural': 'Prodejci'},
        ),
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Pořadí'),
        ),
    ]
