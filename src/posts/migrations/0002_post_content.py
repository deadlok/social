# Generated by Django 4.2.4 on 2023-09-12 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
