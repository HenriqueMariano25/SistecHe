# Generated by Django 3.0.6 on 2020-05-25 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20200524_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='extra_hour',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='leader',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.Sector'),
        ),
    ]
