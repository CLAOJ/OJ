# Generated by Django 2.2.24 on 2022-06-20 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0153_problem_suggester'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='scoreboard_cache_timeout',
            field=models.PositiveIntegerField(default=0, help_text='How long should the scoreboard be cached. Set to 0 to disable caching.', verbose_name='scoreboard cache timeout'),
        ),
    ]
