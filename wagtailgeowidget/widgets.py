import json

import six
from django.forms import HiddenInput
from django.utils.html import format_html
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.point import Point
from django.utils.safestring import mark_safe

from wagtailgeowidget.app_settings import (
    GEO_WIDGET_DEFAULT_LOCATION,
    GEO_WIDGET_ZOOM,
    GOOGLE_MAPS_V3_APIKEY,
)


class GeoField(HiddenInput):
    address_field = None
    srid = None

    class Media:
        css = {
            'all': ('wagtailgeowidget/css/geo-field.css',)
        }

        js = (
            'wagtailgeowidget/js/geo-field.js',
            'https://maps.google.com/maps/api/js?key={}'.format(
                GOOGLE_MAPS_V3_APIKEY
            ),
        )

    def render(self, name, value, attrs=None):
        out = super(GeoField, self).render(name, value, attrs)

        location = format_html(
            '<div class="input">'
            '<input id="_id_{}_latlng" class="geo-field-location" maxlength="250" type="text">'  # NOQA
            '</div>',
            name
        )

        data = {
            'sourceSelector': '#id_{}'.format(name),
            'defaultLocation': GEO_WIDGET_DEFAULT_LOCATION,
            'addressSelector': '#id_{}'.format(self.address_field),
            'latLngDisplaySelector': '#_id_{}_latlng'.format(name),
            'zoom': GEO_WIDGET_ZOOM,
            'srid': self.srid,
        }

        if value and isinstance(value, six.string_types):
            value = GEOSGeometry(value)
            data['defaultLocation'] = {
                'lat': value.y,
                'lng': value.x,
            }

        if value and isinstance(value, Point):
            data['defaultLocation'] = {
                'lat': value.y,
                'lng': value.x,
            }

        json_data = json.dumps(data)
        data_id = 'geo_field_{}_data'.format(name)

        return mark_safe(
            '<script>window.{} = {};</script>'.format(data_id, json_data) +
            out +
            location +
            '<div class="geo-field" data-data-id="{}"></div>'.format(data_id)
        )
