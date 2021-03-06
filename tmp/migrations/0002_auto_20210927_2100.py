# Generated by Django 3.0.5 on 2021-09-27 21:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Experiment', '0002_experiment_name'),
        ('Login', '0001_initial'),
        ('Course', '0001_initial'),
        ('File', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkFile',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(max_length=256)),
                ('file_path', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('course_template_experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.CourseTemplateExperiment')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Experiment.Experiment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.User')),
            ],
        ),
        migrations.DeleteModel(
            name='CourseFile',
        ),
    ]
