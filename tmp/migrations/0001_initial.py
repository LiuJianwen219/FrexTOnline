# Generated by Django 3.0.5 on 2021-09-27 19:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Experiment', '0001_initial'),
        ('Course', '0001_initial'),
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('src', 'src'), ('bit', 'bit'), ('log', 'log'), ('other', 'other'), ('unknown', 'unknown')], max_length=8)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(max_length=256)),
                ('file_path', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Experiment.Experiment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.User')),
            ],
        ),
        migrations.CreateModel(
            name='CourseFile',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(max_length=256)),
                ('file_path', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('course_template_experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.CourseTemplateExperiment')),
            ],
        ),
    ]