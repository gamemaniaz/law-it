# Generated by Django 2.1.2 on 2019-02-02 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatmiddleware', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='admission_date',
            field=models.DateField(default=None),
        ),
    ]
