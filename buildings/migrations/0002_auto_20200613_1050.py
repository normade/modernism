# Generated by Django 3.0.5 on 2020-06-13 10:50

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        ('wagtailimages', '0001_squashed_0021'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('buildings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingpage',
            name='architects',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='people.Architect'),
        ),
        migrations.AddField(
            model_name='buildingpage',
            name='building_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='buildings.BuildingType'),
        ),
        migrations.AddField(
            model_name='buildingpage',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='buildings.City'),
        ),
        migrations.AddField(
            model_name='buildingpage',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='buildings.Country'),
        ),
        migrations.AddField(
            model_name='buildingpage',
            name='developers',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='people.Developer'),
        ),
        migrations.AddField(
            model_name='buildingpage',
            name='feed_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='buildingpage',
            name='owners',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='people.BuildingOwner'),
        ),
        migrations.AddField(
            model_name='buildingpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='buildings.BuildingPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
