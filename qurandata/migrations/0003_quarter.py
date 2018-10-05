# Generated by Django 2.0.4 on 2018-10-04 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qurandata', '0002_auto_20180508_0520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField(verbose_name='Global position of quarter')),
                ('hizb', models.PositiveIntegerField(verbose_name='Index of hizb')),
                ('pos_in_hizb', models.PositiveIntegerField(verbose_name='Posiiton in hizb : 1 to 4')),
                ('endaya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='qurandata.Aya')),
                ('startaya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='qurandata.Aya')),
            ],
        ),
    ]