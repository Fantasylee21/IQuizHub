# Generated by Django 5.0.7 on 2024-07-25 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_questiongroup_is_all'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questiongroup',
            name='questions',
            field=models.ManyToManyField(blank=True, null=True, related_name='question_groups', to='questions.question', verbose_name='问题'),
        ),
    ]
