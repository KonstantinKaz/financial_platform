# Generated by Django 4.2.7 on 2023-11-07 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_remove_account_currency_alter_account_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]