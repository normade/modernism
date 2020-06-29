# Generated by Django 3.0.5 on 2020-06-29 18:44

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0002_auto_20200618_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='country',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]