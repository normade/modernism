from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from django_countries import countries
from django_countries.fields import CountryField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from people.models import ArchitectPage, BuildingOwnerPage, DeveloperPage
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.api import APIField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel

from buildings.blocks import GalleryImageBlock


class Tag(TaggitTag):
    class Meta:
        proxy = True


class BuildingType(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    panels = [FieldPanel("name"), FieldPanel("description", classname="full")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Building types"


class AccessType(models.Model):
    name = models.CharField(max_length=255)
    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Access types"


class Country(models.Model):
    country = CountryField(blank_label="(Select a Country)", unique=True)
    description = RichTextField(blank=True)
    panels = [FieldPanel("country"), FieldPanel("description", classname="full")]

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="cities"
    )
    description = RichTextField(blank=True)
    panels = [
        FieldPanel("name"),
        FieldPanel("country"),
        FieldPanel("description", classname="full"),
    ]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Cities"


class PlacesIndexPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    def clean(self):
        """Override slug."""
        super().clean()
        self.slug = slugify(self.title)


class BuildingsIndexPage(Page):
    subpage_types = ["BuildingPage"]
    parent_page_types = ["home.HomePage"]
    max_count = 1

    ajax_template = "buildings/buildings_list_page.html"
    template = "buildings/buildings_index_page.html"

    def _get_country_code(self, tag_country):
        for code, country in dict(countries).items():
            if tag_country == country:
                return code

    def get_context(self, request):
        context = super().get_context(request)

        architect_id = request.GET.get("architect")
        tag = request.GET.get("tag")
        buildings = BuildingPage.objects.live().order_by("-first_published_at")
        tag_country_name = ""
        tag_building_type = BuildingType.objects.filter(name=tag).first()

        if tag:
            buildings = buildings.filter(tags__name=tag)
            country_code = self._get_country_code(tag)
            if Country.objects.filter(country=country_code).exists():
                tag_country_name = tag

        if architect_id:
            buildings = buildings.filter(architects__architect__id=architect_id)
            context["active_architect"] = ArchitectPage.objects.filter(
                id=architect_id
            ).first()

        context["buildings"] = buildings
        context["tag_country_name"] = tag_country_name
        context["tag_building_type"] = tag_building_type
        context["architects"] = ArchitectPage.objects.exclude(buildings=None).order_by(
            "last_name"
        )
        context["countries"] = (
            Country.objects.exclude(buildingpage=None)
            .prefetch_related(
                models.Prefetch("cities", queryset=City.objects.order_by("name"))
            )
            .order_by("country")
        )
        context["types"] = BuildingType.objects.exclude(buildingpage=None).order_by(
            "name"
        )
        context["years"] = (
            BuildingPage.objects.exclude(year_of_construction__exact="")
            .distinct("year_of_construction")
            .order_by("year_of_construction")
            .values_list("year_of_construction", flat=True)
        )
        return context

    def clean(self):
        """Override slug."""
        super().clean()
        self.slug = slugify(self.title)


class BuildingPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BuildingPageArchitectRelation(models.Model):
    page = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="architects"
    )
    architect = ParentalKey(
        "people.ArchitectPage", on_delete=models.CASCADE, related_name="buildings"
    )
    panels = [
        FieldPanel("architect"),
    ]

    class Meta:
        unique_together = ("page", "architect")


class BuildingPageOwnerRelation(models.Model):
    page = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="owners"
    )
    owner = ParentalKey(
        "people.BuildingOwnerPage", on_delete=models.CASCADE, related_name="buildings"
    )
    panels = [
        FieldPanel("owner"),
    ]

    class Meta:
        unique_together = ("page", "owner")


class BuildingPageDeveloperRelation(models.Model):
    page = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="developers"
    )
    developer = ParentalKey(
        "people.DeveloperPage", on_delete=models.CASCADE, related_name="buildings"
    )
    panels = [
        FieldPanel("developer"),
    ]

    class Meta:
        unique_together = ("page", "developer")


class BuildingPage(Page):
    name = models.CharField(max_length=250, unique=True)
    building_type = models.ForeignKey(
        BuildingType, on_delete=models.SET_NULL, null=True, blank=True,
    )
    access_type = models.ForeignKey(
        AccessType, on_delete=models.SET_NULL, null=True, blank=True,
    )
    todays_use = models.CharField(max_length=300, blank=True)
    description = RichTextField(blank=True)
    year_of_construction = models.CharField(max_length=4, blank=True)
    directions = models.TextField(
        blank=True,
        help_text="Note here how to get there, public transport information or alike.",
    )
    address = models.TextField(
        blank=True, help_text="Please, provide a street name and/or number."
    )
    zip_code = models.CharField(max_length=10, default="00000",)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    lat_long = models.CharField(
        max_length=36,
        help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182) \
                   Right click Google Maps and select 'What's Here'",
        validators=[
            RegexValidator(
                regex=r"^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$",
                message="Lat Long must be a comma-separated numeric lat and long",
                code="invalid_lat_long",
            ),
        ],
    )
    tags = ClusterTaggableManager(through=BuildingPageTag, blank=True)
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="This image will be used to preview the building on the buildings overview page.",
    )
    gallery_images = StreamField([("image", GalleryImageBlock()),], blank=True,)

    content_panels = [
        FieldPanel("name"),
        FieldPanel("building_type"),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("zip_code"), FieldPanel("country"),]),
                FieldRowPanel([FieldPanel("city"), FieldPanel("address"),]),
                FieldRowPanel([FieldPanel("lat_long"),]),
                FieldRowPanel([FieldPanel("directions"),]),
            ],
            heading="Address",
        ),
        InlinePanel("architects", label="Architects"),
        InlinePanel("developers", label="Developers"),
        InlinePanel("owners", label="Owners"),
        FieldPanel("year_of_construction"),
        FieldPanel("access_type"),
        FieldPanel("todays_use"),
        ImageChooserPanel("feed_image"),
        FieldPanel("description", classname="full"),
        StreamFieldPanel("gallery_images"),
    ]

    api_fields = [
        APIField("name"),
        APIField("city"),
        APIField("country"),
        APIField("address"),
        APIField("lat_long"),
        APIField("gallery_images"),
    ]

    parent_page_types = ["buildings.BuildingsIndexPage"]
    subpage_types = []

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = "/" + "/".join(
                s.strip("/") for s in [self.get_parent().url, "tags", tag.slug]
            )
        return tags

    @property
    def get_teaser_tags(self):
        types = BuildingType.objects.all().values_list("name", flat=True)
        tags = self.tags.exclude(name__in=types)
        for tag in tags:
            tag.url = "/" + "/".join(
                s.strip("/") for s in [self.get_parent().url, "tags", tag.slug]
            )
        return tags

    @property
    def get_architects(self):
        return BuildingPageArchitectRelation.objects.filter(page=self)

    def clean(self):
        """Override title and slug."""
        super().clean()
        self.title = self.name
        self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        """Add tags from new values."""
        self.tags.clear()
        if self.building_type:
            self.tags.add(self.building_type.name)
        if self.city:
            self.tags.add(self.city.name)
        if self.country:
            self.tags.add(self.country.country.name)
        if self.year_of_construction:
            self.tags.add(self.year_of_construction)

        super(BuildingPage, self).save()
