# Generated by Django 2.2.16 on 2021-09-16 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='genre', to='reviews.Genre'),
        ),
    ]
