# Generated by Django 2.1.2 on 2019-02-01 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lawyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('job_title', models.CharField(blank=True, default='', max_length=255)),
                ('key_practice_areas', models.CharField(blank=True, default='', max_length=255)),
                ('law_prac_name', models.CharField(blank=True, default='', max_length=255)),
                ('law_prac_type', models.CharField(blank=True, default='', max_length=255)),
                ('email', models.EmailField(blank=True, default='', max_length=70)),
                ('website', models.CharField(blank=True, default='', max_length=255)),
                ('tel', models.CharField(blank=True, default='', max_length=20)),
                ('address', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
    ]
