# Generated by Django 2.1.2 on 2019-02-02 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatmiddleware', '0004_lawyer_cases'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='disciplinary_fault',
            field=models.BooleanField(default=False),
        ),
    ]
