# Generated by Django 5.1.6 on 2025-03-24 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_alter_packages_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='packages',
            old_name='num_review',
            new_name='reviews',
        ),
    ]
