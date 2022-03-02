# Generated by Django 3.2.11 on 2022-01-13 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odata_flow', models.CharField(max_length=100)),
                ('game_set', models.IntegerField()),
                ('team', models.CharField(max_length=26)),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
            ],
        ),
    ]