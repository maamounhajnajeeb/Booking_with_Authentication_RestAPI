# Generated by Django 4.2.4 on 2023-09-01 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_stripe_token_paymenttable_stripetoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymenttable',
            name='user',
        ),
        migrations.AddField(
            model_name='paymenttable',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.booking'),
        ),
    ]
