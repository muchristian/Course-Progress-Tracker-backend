# Generated by Django 4.0.2 on 2022-07-17 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulecrud', '0008_session_course_code_session_course_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
