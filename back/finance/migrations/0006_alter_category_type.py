# Generated by Django 4.2.7 on 2023-12-07 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_alter_transaction_account_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(blank=True, choices=[('income', 'Доход'), ('expense', 'Расход')], max_length=10, null=True),
        ),
    ]
