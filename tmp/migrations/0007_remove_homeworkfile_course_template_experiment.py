# Generated by Django 3.0.5 on 2021-09-28 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('File', '0006_homeworkfile_course_template_experiment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeworkfile',
            name='course_template_experiment',
        ),
    ]