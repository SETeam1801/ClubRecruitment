# Generated by Django 3.0.5 on 2020-05-25 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('pass_word', models.CharField(max_length=200)),
                ('stu_id', models.CharField(max_length=200)),
                ('pho_num', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(default='', max_length=200)),
                ('school', models.CharField(default='', max_length=200)),
                ('club_desc', models.TextField()),
                ('img0', models.CharField(default='', max_length=200)),
                ('img1', models.CharField(default='', max_length=200)),
                ('img2', models.CharField(default='', max_length=200)),
                ('img3', models.CharField(default='', max_length=200)),
                ('img4', models.CharField(default='', max_length=200)),
                ('Admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubRecruitment.Admin')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(default='', max_length=200)),
                ('dept_desc', models.TextField()),
                ('start_time', models.DateTimeField(blank=True, default='2020-5-25 00:00:00', null=True)),
                ('end_time', models.DateTimeField(blank=True, default='2020-5-25 00:00:00', null=True)),
                ('qq', models.CharField(default='', max_length=200)),
                ('times', models.IntegerField(default=1)),
                ('max_num', models.IntegerField(default=0)),
                ('standard', models.CharField(default='', max_length=200)),
                ('add', models.TextField(default='')),
                ('status', models.IntegerField(default=0)),
                ('Club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubRecruitment.Club')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('pass_word', models.CharField(max_length=200)),
                ('stu_id', models.CharField(max_length=200)),
                ('pho_num', models.CharField(max_length=200)),
                ('college', models.CharField(max_length=200)),
                ('stu_class', models.CharField(max_length=200)),
                ('mailbox', models.CharField(max_length=200)),
                ('school', models.CharField(default='', max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recruitment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_name', models.CharField(default='', max_length=200)),
                ('stu_id', models.CharField(default='', max_length=200)),
                ('pho_num', models.CharField(default='', max_length=200)),
                ('mailbox', models.CharField(default='', max_length=200)),
                ('stu_desc', models.TextField()),
                ('stu_status', models.IntegerField(default=1)),
                ('Club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubRecruitment.Club')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubRecruitment.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('text', models.TextField()),
                ('title', models.CharField(default='', max_length=200)),
                ('Club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubRecruitment.Club')),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubRecruitment.Department')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubRecruitment.Student')),
            ],
        ),
    ]
