# Generated by Django 4.0.2 on 2022-02-19 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_alter_comment_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created_at',)},
        ),
    ]