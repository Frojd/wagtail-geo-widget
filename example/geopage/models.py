from __future__ import absolute_import, unicode_literals

from django.contrib.gis.db import models
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtailgeowidget.edit_handlers import GeoPanel


class GeoLocation(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    panels = [
        FieldPanel('title'),
        GeoPanel('location'),
    ]


class GeoPageRelatedLocations(Orderable, GeoLocation):
    page = ParentalKey('geopage.GeoPage', related_name='related_locations')


class GeoPage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoPanel('location'),
        InlinePanel('related_locations', label="Related locations"),
    ]


from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from wagtailgeowidget.blocks import GeoBlock


class GeoStreamPage(Page):
    body = StreamField([
        ('map', GeoBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        data = super(GeoStreamPage, self).get_context(request)
        return data
