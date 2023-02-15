# Generated by Django 4.1.7 on 2023-02-14 15:07

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.TextField()),
                ('response', models.JSONField(default=main.models.tf_response_default, verbose_name='TfResponse')),
                ('request_time', models.DateTimeField()),
                ('response_time', models.DateTimeField()),
            ],
        ),
    ]