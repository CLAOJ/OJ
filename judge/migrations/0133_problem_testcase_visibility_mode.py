# Generated by Django 2.2.24 on 2022-04-05 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0132_allow_blank_sol'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='testcase_visibility_mode',
            field=models.CharField(choices=[('O', 'Visiable for authors'), ('C', 'Visiable if user is not in a contest'), ('A', 'Always visible')], default='C', max_length=1, verbose_name='Testcase visibility'),
        ),
    ]
