# Generated by Django 4.0.2 on 2022-02-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auser', '0002_customuserchannel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuserchannel',
            name='describe',
            field=models.TextField(blank=True, null=True),
        ),
    ]
