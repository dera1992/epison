# Generated by Django 4.1.5 on 2023-07-30 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rename_agent_type_profile_med_type_alter_profile_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='med_type',
            new_name='membership_type',
        ),
    ]
