# Generated by Django 2.1.1 on 2018-09-17 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_auto_20180912_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('user', models.CharField(max_length=20)),
                ('class_name', models.CharField(max_length=40)),
            ],
        ),
    ]