# Generated by Django 3.1.4 on 2020-12-28 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20201226_1501'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name_plural': 'Images for inner content'},
        ),
        migrations.AddField(
            model_name='status',
            name='slug',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
