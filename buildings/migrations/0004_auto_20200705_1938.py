# Generated by Django 3.0.5 on 2020-07-05 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buildings", "0003_auto_20200629_1844"),
    ]

    operations = [
        migrations.AddField(
            model_name="buildingpage",
            name="todays_use",
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name="buildingpage",
            name="address",
            field=models.TextField(
                blank=True, help_text="Please, provide a street name and/or number."
            ),
        ),
    ]
