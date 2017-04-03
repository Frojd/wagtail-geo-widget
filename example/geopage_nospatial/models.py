from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.functional import cached_property
from wagtail.wagtailcore.models import Page
from wagtailgeowidget.edit_handlers import GeoPanel


class StandardPage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        GeoPanel('location', address_field='address'),
    ]

    def get_context(self, request):
        data = super(StandardPage, self).get_context(request)
        return data

    @cached_property
    def point(self):
        from wagtailgeowidget.helpers import parse_geosgeometry_string
        return parse_geosgeometry_string(self.location)

    @property
    def lat(self):
        return self.point['y']

    @property
    def lng(self):
        return self.point['x']


from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore import blocks

from wagtailgeowidget.blocks import GeoBlock


class StreamPage(Page):
    body = StreamField([
        ('map', GeoBlock()),
        ('map_struct', blocks.StructBlock([
            ('address', blocks.CharBlock(required=True)),
            ('map', GeoBlock(address_field='address')),
        ], icon='user'))
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
