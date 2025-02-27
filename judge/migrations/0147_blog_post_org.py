# Generated by Django 2.2.24 on 2022-04-19 03:33

import django.db.models.deletion
from django.db import migrations, models


def apply_global_post(apps, schema_editor):
    BlogPost = apps.get_model('judge', 'BlogPost')
    for post in BlogPost.objects.filter(visible=True).iterator():
        post.global_post = True
        post.save(update_fields=['global_post'])


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0146_new_roles'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'permissions': (('edit_all_post', 'Edit all posts'), ('edit_organization_post', 'Edit organization posts')), 'verbose_name': 'blog post', 'verbose_name_plural': 'blog posts'},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='global_post',
            field=models.BooleanField(default=False, help_text='Display this blog post at the homepage.', verbose_name='global post'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_author_org', to='judge.Organization', verbose_name='organization'),
        ),
        migrations.RunPython(
            apply_global_post, migrations.RunPython.noop, atomic=True,
        ),
    ]
