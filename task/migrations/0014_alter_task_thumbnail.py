# Generated by Django 4.2.2 on 2023-06-13 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_alter_task_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='thumbnail',
            field=models.ImageField(blank=True, default='note_ml5jgv.jpg', upload_to='images/'),
        ),
    ]
