import six
from django import forms
from django.utils.functional import cached_property
from wagtail.core.blocks import CharBlock, FieldBlock

from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtailgeowidget.widgets import GeoField


class GeoAddressBlock(CharBlock):
    class Meta:
        classname = "geo-address-block"


class GeoBlock(FieldBlock):
    class Meta:
        icon = "site"

    def __init__(
        self, address_field=None, required=True, help_text=None, **kwargs
    ):
        self.field_options = {}
        self.address_field = address_field
        super(GeoBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {'widget': GeoField(
            srid=4326,
            id_prefix='',
            address_field=self.address_field,
            used_in="GeoBlock",
        )}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_form(self, value, prefix='', errors=None):
        if value and isinstance(value, dict):
            value = "SRID={};POINT({} {})".format(
                value['srid'],
                value['lng'],
                value['lat'],
            )

        return super(GeoBlock, self).render_form(value, prefix, errors)

    def value_from_form(self, value):
        return value

    def value_for_form(self, value):
        if not value:
            return None

        if value and isinstance(value, six.string_types):
            return value

        val = "SRID={};POINT({} {})".format(
            4326,
            value['lng'],
            value['lat'],
        )
        return val

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
