# Generated by Django 2.2.4 on 2019-09-10 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0006_auto_20190910_1337"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review", name="date", field=models.DateField(auto_now_add=True),
        ),
    ]
