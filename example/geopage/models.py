from __future__ import absolute_import, unicode_literals

from django.contrib.gis.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)

from wagtail.wagtailcore import blocks
from modelcluster.fields import ParentalKey
from wagtailgeowidget.edit_handlers import GeoPanel


class GeoLocation(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    panels = [
        FieldPanel('title'),
        MultiFieldPanel([
            FieldPanel('address'),
            GeoPanel('location', address_field='address')
        ], _('Geo details')),
    ]


class GeoPageRelatedLocations(Orderable, GeoLocation):
    page = ParentalKey('geopage.GeoPage', related_name='related_locations')


class GeoPage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel('related_locations', label="Related locations"),
    ]

    location_panels = [
        MultiFieldPanel([
            FieldPanel('address'),
            GeoPanel('location', address_field='address'),
        ], heading='Location')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(location_panels, heading='Location'),
        ObjectList(Page.settings_panels, heading='Settings',
                   classname="settings"),
    ])


from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from wagtailgeowidget.blocks import GeoBlock


class GeoStreamPage(Page):
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

    def get_context(self, request):
        data = super(GeoStreamPage, self).get_context(request)
        return data


class ClassicGeoPage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('address'),
            GeoPanel('location', address_field='address'),
        ], _('Geo details')),
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
        return self.point['y']

    @property
    def lng(self):
        return self.point['x']
