# Generated by Django 5.2.1 on 2025-05-22 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('location', models.CharField(max_length=255, verbose_name='location')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('subjects', models.JSONField(help_text='Type each subjects separated with a comma', max_length=255, verbose_name='subject')),
            ],
            options={
                'verbose_name': 'Trainer',
                'verbose_name_plural': 'Trainers',
                'ordering': ['name', 'subjects'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('location', models.CharField(max_length=255, verbose_name='location')),
                ('participants', models.PositiveIntegerField(default=1, verbose_name='participants')),
                ('date_scheduled', models.DateField(verbose_name='date')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('price', models.PositiveBigIntegerField(default=0, verbose_name='price')),
                ('trainer_price', models.PositiveBigIntegerField(default=0, verbose_name='trainer price')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='course.trainer', verbose_name='trainer')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'ordering': ['name', 'subject'],
            },
        ),
    ]
