# Generated by Django 3.0.5 on 2021-09-28 23:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Experiment', '0006_auto_20210928_0958'),
        ('Login', '0001_initial'),
        ('Class', '0001_initial'),
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
                ('class_homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class.ClassHomework')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Experiment.Experiment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.User')),
            ],
        ),
    ]
