# Generated by Django 3.0.5 on 2020-06-18 22:47

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("people", "0001_initial"),
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("wagtailimages", "0001_squashed_0021"),
        ("buildings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="buildingpageownerrelation",
            name="owner",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="buildings",
                to="people.BuildingOwnerPage",
            ),
        ),
        migrations.AddField(
            model_name="buildingpageownerrelation",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owners",
                to="buildings.BuildingPage",
            ),
        ),
        migrations.AddField(
            model_name="buildingpagedeveloperrelation",
            name="developer",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="buildings",
                to="people.DeveloperPage",
            ),
        ),
        migrations.AddField(
            model_name="buildingpagedeveloperrelation",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="developers",
                to="buildings.BuildingPage",
            ),
        ),
        migrations.AddField(
            model_name="buildingpagearchitectrelation",
            name="architect",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="buildings",
                to="people.ArchitectPage",
            ),
        ),
        migrations.AddField(
            model_name="buildingpagearchitectrelation",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="architects",
                to="buildings.BuildingPage",
            ),
        ),
        migrations.AddField(
            model_name="buildingpage",
            name="building_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="buildings.BuildingType",
            ),
        ),
        migrations.AddField(
            model_name="buildingpage",
            name="city",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="buildings.City",
            ),
        ),
        migrations.AddField(
            model_name="buildingpage",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="buildings.Country",
            ),
        ),
        migrations.AddField(
            model_name="buildingpage",
            name="feed_image",
            field=models.ForeignKey(
                blank=True,
                help_text="This image will be used to preview the building on the buildings overview page.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.Image",
            ),
        ),
        migrations.AddField(
            model_name="buildingpage",
            name="tags",
            field=modelcluster.contrib.taggit.ClusterTaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="buildings.BuildingPageTag",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="buildingpageownerrelation", unique_together={("page", "owner")},
        ),
        migrations.AlterUniqueTogether(
            name="buildingpagedeveloperrelation",
            unique_together={("page", "developer")},
        ),
        migrations.AlterUniqueTogether(
            name="buildingpagearchitectrelation",
            unique_together={("page", "architect")},
        ),
    ]
