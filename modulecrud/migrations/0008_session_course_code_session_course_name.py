# Generated by Django 4.0.2 on 2022-05-10 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulecrud', '0007_session_department_alter_course_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='course_code',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='course_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]