# Generated by Django 4.2.1 on 2024-05-28 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_alter_productos_producto_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='producto_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
