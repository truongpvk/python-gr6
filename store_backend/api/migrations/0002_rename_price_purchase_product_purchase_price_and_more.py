# Generated by Django 5.0.6 on 2024-07-16 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="price_purchase",
            new_name="purchase_price",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="price_selling",
            new_name="selling_price",
        ),
    ]
