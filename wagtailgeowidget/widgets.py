import json

import six
from django.conf import settings
from django.forms import HiddenInput
from django.utils.html import format_html
from django.contrib.gis.geos import GEOSGeometry
from django.utils.safestring import mark_safe


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
                settings.GOOGLE_MAPS_V3_APIKEY
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
            'defaultLocation':  None,
            'addressSelector': '#id_{}'.format(self.address_field),
            'latLngDisplaySelector': '#_id_{}_latlng'.format(name),
            'zoom': 7,
            'srid': self.srid,
        }

        if value and isinstance(value, six.string_types):
            value = GEOSGeometry(value)

        if value:
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
