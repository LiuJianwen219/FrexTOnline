# Generated by Django 3.0.5 on 2021-09-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Experiment', '0005_auto_20210928_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='compilerecord',
            name='compile_end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='compilerecord',
            name='compile_start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
