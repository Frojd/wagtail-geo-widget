from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from wagtailgeowidget.edit_handlers import GeoPanel
from wagtailgeowidget.blocks import GeoBlock


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
        data = super(StandardPage, self).get_context(request)
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
                        # ('map', GeoBlock(address_field='address')),
                    ],
                    icon="user",
                ),
            ),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]
