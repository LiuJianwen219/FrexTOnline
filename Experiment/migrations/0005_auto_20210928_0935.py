# Generated by Django 3.0.5 on 2021-09-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Experiment', '0004_auto_20210928_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compilerecord',
            name='status',
            field=models.CharField(max_length=256),
        ),
    ]
