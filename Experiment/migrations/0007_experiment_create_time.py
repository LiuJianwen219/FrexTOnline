# Generated by Django 3.0.5 on 2021-10-07 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Experiment', '0006_auto_20210928_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]