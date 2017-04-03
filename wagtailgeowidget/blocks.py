from django import forms
from django.utils.functional import cached_property
from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtail.wagtailcore.blocks import FieldBlock

from wagtailgeowidget.widgets import GeoField
from wagtailgeowidget.app_settings import (
    GEO_WIDGET_DEFAULT_LOCATION,
)


class GeoBlock(FieldBlock):
    def __init__(self, address_field=None, required=True, help_text=None,
                 **kwargs):
        self.field_options = {}
        self.address_field = address_field
        super(GeoBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {'widget': GeoField(
            srid=4326,
            id_prefix='',
            address_field=self.address_field,
        )}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def clean(self, value):
        if not value:
            value = "SRID={};POINT({} {})".format(
                4326,
                GEO_WIDGET_DEFAULT_LOCATION['lng'],
                GEO_WIDGET_DEFAULT_LOCATION['lat']
            )
        return super(GeoBlock, self).clean(value)

    def render_form(self, value, prefix='', errors=None):
        if value and isinstance(value, dict):
            value = "SRID={};POINT({} {})".format(value['srid'],
                                                  value['lng'],
                                                  value['lat'])
        return super(GeoBlock, self).render_form(value, prefix, errors)

    def to_python(self, value):
        if isinstance(value, dict):
            return value

        value = geosgeometry_str_to_struct(value)
        value = {
            'lat': value['y'],
            'lng': value['x'],
            'srid': value['srid'],
        }

        return super(GeoBlock, self).to_python(value)
