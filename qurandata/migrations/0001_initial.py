# Generated by Django 2.0.4 on 2018-05-08 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ['sura', 'index'],
            },
        ),
        migrations.CreateModel(
            name='Sura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('ayas', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['index'],
            },
        ),
        migrations.AddField(
            model_name='aya',
            name='sura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qurandata.Sura'),
        ),
    ]
