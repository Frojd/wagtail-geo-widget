from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtailgeowidget.blocks import GeoAddressBlock, GeoBlock, GeoZoomBlock
from wagtailgeowidget.edit_handlers import GeoPanel


class StandardPage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("address"),
                GeoPanel("location", address_field="address"),
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
                FieldPanel("address"),
                FieldPanel("zoom"),
                GeoPanel("location", address_field="address", zoom_field="zoom"),
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
    body = StreamField(
        [
            ("map", GeoBlock()),
            (
                "map_struct",
                blocks.StructBlock(
                    [
                        ("address", blocks.CharBlock(required=True)),
                        ("map", GeoBlock(address_field="address")),
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
                        ("map", GeoBlock(address_field="address", zoom_field="zoom")),
                    ],
                    icon="user",
                ),
            ),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]
