# Generated by Django 3.0.5 on 2020-05-13 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubRecruitment', '0003_student_school'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='shool',
            new_name='school',
        ),
    ]