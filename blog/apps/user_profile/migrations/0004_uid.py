# Generated by Django 3.2.4 on 2021-06-23 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_alter_account_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(verbose_name='uuid')),
                ('user_id', models.BigIntegerField(verbose_name='user_id')),
            ],
            options={
                'db_table': 'uid',
            },
        ),
    ]
