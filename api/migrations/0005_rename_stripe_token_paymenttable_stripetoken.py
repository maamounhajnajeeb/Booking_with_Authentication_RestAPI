# Generated by Django 4.2.4 on 2023-09-01 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_booking_paid_paymenttable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymenttable',
            old_name='stripe_token',
            new_name='stripeToken',
        ),
    ]
