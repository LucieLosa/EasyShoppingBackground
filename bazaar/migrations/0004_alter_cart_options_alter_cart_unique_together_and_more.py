# Generated by Django 4.2 on 2023-09-21 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0003_alter_eventseller_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['event', 'identifier']},
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='eventseller',
            unique_together={('event', 'seller')},
        ),
        migrations.AddField(
            model_name='cart',
            name='identifier',
            field=models.CharField(default='A01', max_length=128, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventseller',
            name='identifier',
            field=models.PositiveSmallIntegerField(verbose_name='Seller identifier'),
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('identifier', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='eventseller',
            unique_together={('event', 'seller'), ('event', 'identifier')},
        ),
        migrations.RemoveField(
            model_name='cart',
            name='name',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='number',
        ),
    ]
