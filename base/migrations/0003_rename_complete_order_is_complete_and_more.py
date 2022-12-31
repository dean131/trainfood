# Generated by Django 4.1.4 on 2022-12-14 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_product_product_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='complete',
            new_name='is_complete',
        ),
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='order',
            name='is_done',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='is_recomended',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(null=True, verbose_name=1000),
        ),
    ]