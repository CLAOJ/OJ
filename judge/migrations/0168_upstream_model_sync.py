import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('judge', '0152_deactivate_user_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='class_required',
            field=models.BooleanField(default=False, verbose_name='class membership required',
                                      help_text='Whether members are compelled to select a class when joining.'),
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='class name')),
                ('slug', models.SlugField(max_length=128, verbose_name='class slug',
                                          help_text='Class name shown in URLs.')),
                ('description', models.TextField(blank=True, verbose_name='class description')),
                ('is_active', models.BooleanField(default=True, verbose_name='is class active')),
                ('access_code', models.CharField(blank=True, max_length=7, null=True,
                                                 verbose_name='access code', help_text='Student access code.')),
                ('admins', models.ManyToManyField(to='judge.Profile', related_name='class_admin_of',
                                                  verbose_name='administrators',
                                                  help_text='Those who can approve membership to this class.')),
                ('members', models.ManyToManyField(to='judge.Profile', blank=True, related_name='classes',
                                                   related_query_name='class', verbose_name='members')),
                ('organization', models.ForeignKey(to='judge.Organization', on_delete=django.db.models.deletion.CASCADE,
                                                   related_name='classes', related_query_name='class',
                                                   verbose_name='organization',
                                                   help_text='The organization that this class belongs to.')),
            ],
            options={
                'verbose_name': 'class',
                'verbose_name_plural': 'classes',
                'ordering': ['organization', 'name'],
            },
        ),
        migrations.AddField(
            model_name='contest',
            name='classes',
            field=models.ManyToManyField(
                to='judge.Class', blank=True, verbose_name='classes',
                help_text='If organization private, only these classes may see the contest.',
            ),
        ),
        migrations.AddField(
            model_name='organizationrequest',
            name='request_class',
            field=models.ForeignKey(to='judge.Class', null=True, blank=True,
                                    on_delete=django.db.models.deletion.CASCADE, verbose_name='class'),
        ),
        migrations.AddField(
            model_name='contest',
            name='view_contest_submissions',
            field=models.ManyToManyField(
                to='judge.Profile', blank=True, related_name='view_contest_submissions',
                verbose_name='can see contest submissions',
                help_text='These users will be able to see in-contest submissions.',
            ),
        ),
        migrations.AddField(
            model_name='contest',
            name='limit_join_organizations',
            field=models.BooleanField(default=False, verbose_name='limit organizations that can join'),
        ),
        migrations.AddField(
            model_name='contest',
            name='join_organizations',
            field=models.ManyToManyField(
                to='judge.Organization', blank=True, related_name='join_only_contests',
                verbose_name='join organizations',
                help_text='If non-empty, only these organizations may join the contest.',
            ),
        ),
        migrations.AddField(
            model_name='contest',
            name='tester_see_scoreboard',
            field=models.BooleanField(default=False, verbose_name='testers see scoreboard',
                                      help_text='If testers can see the scoreboard.'),
        ),
        migrations.AddField(
            model_name='contest',
            name='tester_see_submissions',
            field=models.BooleanField(default=False, verbose_name='testers see submissions',
                                      help_text='If testers can see in-contest submissions.'),
        ),
        migrations.AddField(
            model_name='contest',
            name='spectators',
            field=models.ManyToManyField(
                to='judge.Profile', blank=True, related_name='spectated_contests',
                verbose_name='spectators',
                help_text=(
                    'These users will be able to spectate the contest, '
                    'but not see the problems ahead of time.'
                ),
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_banned_from_problem_voting',
            field=models.BooleanField(default=False, verbose_name='banned from voting on problem point values',
                                      help_text="User will not be able to vote on problems' point values."),
        ),
        migrations.CreateModel(
            name='ProblemPointsVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(verbose_name='proposed points',
                                               help_text='The amount of points the voter thinks this problem deserves.',
                                               validators=[django.core.validators.MinValueValidator(1),
                                                           django.core.validators.MaxValueValidator(50)])),
                ('note', models.TextField(blank=True, default='', max_length=8192, verbose_name='note',
                                          help_text='Justification for problem point value.')),
                ('vote_time', models.DateTimeField(auto_now_add=True, verbose_name='vote time',
                                                   help_text='The time this vote was cast.')),
                ('problem', models.ForeignKey(to='judge.Problem', related_name='problem_points_votes',
                                              on_delete=django.db.models.deletion.CASCADE, verbose_name='problem')),
                ('voter', models.ForeignKey(to='judge.Profile', related_name='problem_points_votes',
                                            on_delete=django.db.models.deletion.CASCADE, verbose_name='voter')),
            ],
            options={
                'verbose_name': 'problem vote',
                'verbose_name_plural': 'problem votes',
            },
        ),
        migrations.AlterModelOptions(
            name='problem',
            options={'permissions': (
                ('see_private_problem', 'See hidden problems'),
                ('edit_own_problem', 'Edit own problems'),
                ('create_organization_problem', 'Create organization problem'),
                ('edit_all_problem', 'Edit all problems'),
                ('edit_public_problem', 'Edit all public problems'),
                ('suggest_new_problem', 'Suggest new problem'),
                ('problem_full_markup', 'Edit problems with full markup'),
                ('clone_problem', 'Clone problem'),
                ('upload_file_statement', 'Upload file-type statement'),
                ('change_public_visibility', 'Change is_public field'),
                ('change_manually_managed', 'Change is_manually_managed field'),
                ('see_organization_problem', 'See organization-private problems'),
                ('create_private_problem', 'Create private problems'),
            ), 'verbose_name': 'problem', 'verbose_name_plural': 'problems'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': (
                ('test_site', 'Shows in-progress development stuff'),
                ('totp', 'Edit TOTP settings'),
                ('high_problem_timelimit', 'Can set high problem timelimit'),
                ('long_contest_duration', 'Can set long contest duration'),
                ('upload_image_server', 'Can upload image to server'),
                ('deactivate_users', 'Deactivate users'),
            ), 'verbose_name': 'user profile', 'verbose_name_plural': 'user profiles'},
        ),
    ]
