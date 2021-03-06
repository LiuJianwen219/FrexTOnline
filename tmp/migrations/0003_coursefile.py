# Generated by Django 3.0.5 on 2021-09-27 21:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0001_initial'),
        ('File', '0002_auto_20210927_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseFile',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=256)),
                ('file_path', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('delete_time', models.DateTimeField()),
                ('course_template_experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.CourseTemplateExperiment')),
            ],
        ),
    ]
