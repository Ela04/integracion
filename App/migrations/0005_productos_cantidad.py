# Generated by Django 4.2.1 on 2024-05-28 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_productos_producto_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
