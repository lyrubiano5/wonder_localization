# Generated by Django 4.1.4 on 2022-12-16 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=50)),
                ('distance', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('antenna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localization.antenna')),
            ],
        ),
    ]
