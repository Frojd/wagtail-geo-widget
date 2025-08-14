from django.contrib.gis.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page

from wagtailgeowidget import geocoders
from wagtailgeowidget.blocks import (
    GeoAddressBlock,
    GeoZoomBlock,
    GoogleMapsBlock,
    LeafletBlock,
)
from wagtailgeowidget.panels import GeoAddressPanel, GoogleMapsPanel, LeafletPanel


class GeoLocation(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=250, blank=True, null=True)
    zoom = models.SmallIntegerField(blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS_PLACES_NEW),
                FieldPanel("zoom"),
                GoogleMapsPanel("location", address_field="address", zoom_field="zoom"),
            ],
            _("Geo details"),
        ),
    ]


class GeoPageRelatedLocations(Orderable, GeoLocation):
    page = ParentalKey(
        "geopage.GeoPage", related_name="related_locations", on_delete=models.CASCADE
    )


class GeoPage(Page):
    page_description = "Google maps with google maps geocoder"

    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel("related_locations", label="Related locations"),
    ]

    location_panels = [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS),
                GoogleMapsPanel("location", address_field="address"),
            ],
            heading="Location",
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(location_panels, heading="Location"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )


class GeoPageWithPlacesNewGeocoderRelatedLocations(Orderable, GeoLocation):
    page = ParentalKey(
        "geopage.GeoPageWithPlacesNewGeocoder",
        related_name="related_locations",
        on_delete=models.CASCADE,
    )


class GeoPageWithPlacesNewGeocoder(Page):
    page_description = "Google maps with google maps geocoder"

    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel("related_locations", label="Related locations"),
    ]

    location_panels = [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS_PLACES_NEW),
                GoogleMapsPanel("location", address_field="address"),
            ],
            heading="Location",
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(location_panels, heading="Location"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings"),
        ]
    )


class GeoLocationWithLeaflet(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(
        max_length=250,
        help_text=_("Search powered by Nominatim"),
        blank=True,
        null=True,
    )
    zoom = models.SmallIntegerField(blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.NOMINATIM),
                FieldPanel("zoom"),
                LeafletPanel("location", address_field="address", zoom_field="zoom"),
            ],
            _("Geo details"),
        ),
    ]


class GeoPageWithLeafletRelatedLocations(Orderable, GeoLocationWithLeaflet):
    page = ParentalKey(
        "geopage.GeoPageWithLeaflet",
        related_name="related_locations",
        on_delete=models.CASCADE,
    )


class GeoPageWithLeaflet(Page):
    page_description = "Leaflet with nominatim geocoder"

    address = models.CharField(
        max_length=250,
        help_text=_("Search powered by Nominatim"),
        blank=True,
        null=True,
    )
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel("related_locations", label="Related locations"),
    ]

    location_panels = [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.NOMINATIM),
                LeafletPanel("location", address_field="address"),
            ],
            heading="Location",
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(location_panels, heading="Location"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )


class GeoStreamPage(Page):
    page_description = "All map blocks"

    streamfield_params = {}

    body = StreamField(
        [
            ("map", GoogleMapsBlock()),
            ("map_with_leaflet", LeafletBlock()),
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
                "map_struct_with_deprecated_geocoder_places",
                blocks.StructBlock(
                    [
                        (
                            "address",
                            GeoAddressBlock(
                                required=True, geocoder=geocoders.GOOGLE_MAPS_PLACES
                            ),
                        ),
                        ("map", GoogleMapsBlock(address_field="address")),
                    ],
                    icon="user",
                ),
            ),
            (
                "map_struct_with_geocoder_places_new",
                blocks.StructBlock(
                    [
                        (
                            "address",
                            GeoAddressBlock(
                                required=True, geocoder=geocoders.GOOGLE_MAPS_PLACES_NEW
                            ),
                        ),
                        ("map", GoogleMapsBlock(address_field="address")),
                    ],
                    icon="user",
                ),
            ),
            (
                "map_struct_with_leaflet",
                blocks.StructBlock(
                    [
                        ("address", GeoAddressBlock(required=True)),
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

    def get_context(self, request):
        data = super(GeoStreamPage, self).get_context(request)
        return data


class ClassicGeoPage(Page):
    page_description = "Google maps with google maps places geocoder"

    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS_PLACES),
                GoogleMapsPanel("location", address_field="address", hide_latlng=True),
            ],
            _("Geo details"),
        ),
    ]

    def get_context(self, request):
        data = super(ClassicGeoPage, self).get_context(request)
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


class ClassicGeoPageWithLeaflet(Page):
    page_description = "Leaflet with mapbox geocoder"

    address = models.CharField(
        max_length=250,
        help_text=_("Search powered by MapBox"),
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.MAPBOX),
                LeafletPanel("location", address_field="address", hide_latlng=True),
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


class ClassicGeoPageWithZoom(Page):
    page_description = "Google maps with google maps geocoder"

    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    zoom = models.SmallIntegerField(blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS),
                FieldPanel("zoom"),
                GoogleMapsPanel(
                    "location",
                    address_field="address",
                    zoom_field="zoom",
                    hide_latlng=True,
                ),
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


class ClassicGeoPageWithLeafletAndZoom(Page):
    page_description = "Leaflet with nominatim geocoder"

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
                LeafletPanel(
                    "location",
                    address_field="address",
                    zoom_field="zoom",
                    hide_latlng=True,
                ),
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
