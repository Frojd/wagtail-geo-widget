import json

import six
from django.forms import HiddenInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe

try:
    from django.contrib.gis.geos.point import Point
except:
    Point = None

from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtailgeowidget.app_settings import (
    GEO_WIDGET_DEFAULT_LOCATION,
    GEO_WIDGET_ZOOM,
    GOOGLE_MAPS_V3_APIKEY,
)


class GeoField(HiddenInput):
    address_field = None
    id_prefix = 'id_'
    srid = None

    def __init__(self, *args, **kwargs):
        self.address_field = kwargs.pop('address_field', self.address_field)
        self.srid = kwargs.pop('srid', self.srid)
        self.id_prefix = kwargs.pop('id_prefix', self.id_prefix)

        super(GeoField, self).__init__(*args, **kwargs)

    class Media:
        css = {
            'all': ('wagtailgeowidget/css/geo-field.css',)
        }

        js = (
            'wagtailgeowidget/js/geo-field.js',
            'https://maps.google.com/maps/api/js?key={}&libraries=places'
            .format(
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

        if '-' in name:
            namespace = name.split('-')[:-1]
            namespace = '-'.join(namespace)
            namespace = '{}-'.format(namespace)
        else:
            namespace = ''

        source_selector = '#{}{}'.format(self.id_prefix, name)
        address_selector = '#{}{}{}'.format(self.id_prefix,
                                            namespace,
                                            self.address_field)

        data = {
            'sourceSelector': source_selector,
            'defaultLocation': GEO_WIDGET_DEFAULT_LOCATION,
            'addressSelector': address_selector,
            'latLngDisplaySelector': '#_id_{}_latlng'.format(name),
            'zoom': GEO_WIDGET_ZOOM,
            'srid': self.srid,
        }

        if value and isinstance(value, six.string_types):
            result = geosgeometry_str_to_struct(value)
            if result:
                data['defaultLocation'] = {
                    'lat': result['y'],
                    'lng': result['x'],
                }

        if value and Point and isinstance(value, Point):
            data['defaultLocation'] = {
                'lat': value.y,
                'lng': value.x,
            }

        json_data = json.dumps(data)
        data_id = 'geo_field_{}_data'.format(name)

        return mark_safe(
            '<script>window["{}"] = {};</script>'.format(data_id, json_data) +
            out +
            location +
            '<div class="geo-field" data-data-id="{}"></div>'.format(data_id) +
            """
            <script>
            (function(){
                if (document.readyState === 'complete') {
                    return initializeGeoFields();
                }

                $(window).load(function() {
                    initializeGeoFields();
                });
            })();
            </script>
            """
        )
