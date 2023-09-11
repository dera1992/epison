# Generated by Django 4.1.5 on 2023-05-31 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timebreakdown',
            options={'verbose_name': 'TimeBreakdown', 'verbose_name_plural': 'TimeBreakdown'},
        ),
        migrations.AddField(
            model_name='timebreakdown',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='timebreakdown', to='conference.event'),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='ad_image',
            field=models.ImageField(blank=True, default='profile/None/no_image.png', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speaker', to='conference.event'),
        ),
    ]