from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtailgeowidget import geocoders
from wagtailgeowidget.blocks import (
    GeoAddressBlock,
    GeoBlock,
    GeoZoomBlock,
    GoogleMapsBlock,
    LeafletBlock,
)
from wagtailgeowidget.panels import GeoAddressPanel, GoogleMapsPanel, LeafletPanel


class StandardPage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS),
                GoogleMapsPanel("location", address_field="address"),
            ],
            _("Geo details"),
        ),
    ]

    def get_context(self, request):
        data = super().get_context(request)
        return data

    @cached_property
    def point(self):
        from wagtailgeowidget.helpers import geosgeometry_str_to_struct

        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point["y"]

    @property
    def lng(self):
        return self.point["x"]


class StandardPageWithLeaflet(Page):
    address = models.CharField(
        max_length=250,
        help_text=_("Search powered by Nominatim"),
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.NOMINATIM),
                LeafletPanel("location", address_field="address"),
            ],
            _("Geo details"),
        ),
    ]

    def get_context(self, request):
        data = super().get_context(request)
        return data

    @cached_property
    def point(self):
        from wagtailgeowidget.helpers import geosgeometry_str_to_struct

        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point["y"]

    @property
    def lng(self):
        return self.point["x"]


class StandardPageWithZoom(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    zoom = models.SmallIntegerField(blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS),
                FieldPanel("zoom"),
                GoogleMapsPanel("location", address_field="address", zoom_field="zoom"),
            ],
            _("Geo details"),
        ),
    ]

    def get_context(self, request):
        data = super().get_context(request)
        return data

    @cached_property
    def point(self):
        from wagtailgeowidget.helpers import geosgeometry_str_to_struct

        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point["y"]

    @property
    def lng(self):
        return self.point["x"]


class StandardPageWithLeafletAndZoom(Page):
    address = models.CharField(
        max_length=250,
        help_text=_("Search powered by Nominatim"),
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=250, blank=True, null=True)
    zoom = models.SmallIntegerField(blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.NOMINATIM),
                FieldPanel("zoom"),
                LeafletPanel("location", address_field="address", zoom_field="zoom"),
            ],
            _("Geo details"),
        ),
    ]

    def get_context(self, request):
        data = super().get_context(request)
        return data

    @cached_property
    def point(self):
        from wagtailgeowidget.helpers import geosgeometry_str_to_struct

        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point["y"]

    @property
    def lng(self):
        return self.point["x"]


class StreamPage(Page):
    streamfield_params = {"use_json_field": True} if WAGTAIL_VERSION < (6, 0) else {}

    body = StreamField(
        [
            ("map", GoogleMapsBlock()),
            ("map_leaflet", LeafletBlock()),
            (
                "map_struct",
                blocks.StructBlock(
                    [
                        ("address", GeoAddressBlock(required=True)),
                        ("map", GoogleMapsBlock(address_field="address")),
                    ],
                    icon="user",
                ),
            ),
            (
                "map_struct_with_deprecated_geopanel",
                blocks.StructBlock(
                    [
                        ("address", blocks.CharBlock(required=True)),
                        ("map", GeoBlock(address_field="address")),
                    ],
                    icon="user",
                ),
            ),
            (
                "map_struct_leaflet",
                blocks.StructBlock(
                    [
                        (
                            "address",
                            GeoAddressBlock(required=True, geocoder=geocoders.MAPBOX),
                        ),
                        ("map", LeafletBlock(address_field="address")),
                    ],
                    icon="user",
                ),
            ),
            (
                "map_struct_with_zoom",
                blocks.StructBlock(
                    [
                        ("address", GeoAddressBlock(required=True)),
                        ("zoom", GeoZoomBlock(required=False)),
                        (
                            "map",
                            GoogleMapsBlock(address_field="address", zoom_field="zoom"),
                        ),
                    ],
                    icon="user",
                ),
            ),
            (
                "map_struct_leaflet_with_zoom",
                blocks.StructBlock(
                    [
                        ("address", GeoAddressBlock(required=True)),
                        ("zoom", GeoZoomBlock(required=False)),
                        (
                            "map",
                            LeafletBlock(address_field="address", zoom_field="zoom"),
                        ),
                    ],
                    icon="user",
                ),
            ),
        ],
        **streamfield_params,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
