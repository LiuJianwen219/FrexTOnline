# Generated by Django 3.0.5 on 2021-10-23 10:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Experiment', '0008_compilerecord_file_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='burnrecord',
            old_name='burn_time',
            new_name='burn_start_time',
        ),
        migrations.RemoveField(
            model_name='burnrecord',
            name='file_uid',
        ),
        migrations.AddField(
            model_name='burnrecord',
            name='burn_over_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='burnrecord',
            name='file',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='experimentrecord',
            name='device',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='burnrecord',
            name='status',
            field=models.CharField(choices=[('success', 'success'), ('fail', 'fail')], default='unknown', max_length=8),
        ),
    ]