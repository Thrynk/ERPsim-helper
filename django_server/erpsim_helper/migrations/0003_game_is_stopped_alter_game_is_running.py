# Generated by Django 4.0.3 on 2022-03-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpsim_helper', '0002_game_is_running'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_stopped',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='is_running',
            field=models.BooleanField(default=True, verbose_name='Running'),
        ),
    ]