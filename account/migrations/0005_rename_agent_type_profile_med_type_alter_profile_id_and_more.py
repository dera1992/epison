# Generated by Django 4.1.5 on 2023-04-15 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20191107_0348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='agent_type',
            new_name='med_type',
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='type',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
