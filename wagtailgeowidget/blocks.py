import six
from django import forms
from django.utils.functional import cached_property
from wagtail.core.blocks import CharBlock, FieldBlock

from wagtailgeowidget.app_settings import GEO_WIDGET_ZOOM
from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtailgeowidget.widgets import GeoField


class GeoAddressBlock(CharBlock):
    class Meta:
        classname = "geo-address-block"


class GeoBlock(FieldBlock):
    class Meta:
        icon = "site"

    def __init__(
        self, address_field=None, hide_latlng=False, required=True, help_text=None, **kwargs
    ):
        self.field_options = {}
        self.address_field = address_field
        self.hide_latlng = hide_latlng
        super(GeoBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {'widget': GeoField(
            srid=4326,
            id_prefix='',
            address_field=self.address_field,
            hide_latlng=self.hide_latlng,
            used_in="GeoBlock",
        )}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_form(self, value, prefix='', errors=None):
        print(value)
        if value and isinstance(value, dict):
            value = "SRID={};POINT({} {});ZOOMLEVEL={}".format(
                value['srid'],
                value['lng'],
                value['lat'],
                value['zoom'],
            )

        return super(GeoBlock, self).render_form(value, prefix, errors)

    def value_from_form(self, value):
        return value

    def value_for_form(self, value):
        if not value:
            return None

        if value and isinstance(value, six.string_types):
            return value

        val = "SRID={};POINT({} {});ZOOMLEVEL={}".format(
            4326,
            value['lng'],
            value['lat'],
            value['zoom'],
        )
        return val

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        # get rid of zoom level
        # check if zoom level has been saved to the DB
        if value.find(';ZOOM') != -1:
            geo_value = geosgeometry_str_to_struct(value[:value.find(';ZOOM')])
            zoom_splitted = value.split(';ZOOMLEVEL=')

            if zoom_splitted is not None:
                zoom_level = int(value.split(';ZOOMLEVEL=')[1])
        else:
            geo_value = geosgeometry_str_to_struct(value)
            zoom_level = GEO_WIDGET_ZOOM

        value = {
            'lat': geo_value['y'],
            'lng': geo_value['x'],
            'srid': geo_value['srid'],
            'zoom': zoom_level,
        }

        return super(GeoBlock, self).to_python(value)
