# Generated by Django 2.2 on 2019-08-06 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.FileField(default='noimage.jpg', upload_to=''),
        ),
    ]
