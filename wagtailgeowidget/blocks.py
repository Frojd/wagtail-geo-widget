import json
import six

from django import forms
from django.utils.functional import cached_property
from wagtail.wagtailcore.blocks import FieldBlock

from wagtailgeowidget.widgets import GeoField


class GeoBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field_options = {}
        super(GeoBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {'widget': GeoField(
            srid=4326,
            id_prefix='',
            data_source='json',
        )}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def to_python(self, value):
        if isinstance(value, six.string_types):
            value = json.loads(value)
        return value

    def get_prep_value(self, value):
        if isinstance(value, dict):
            value = json.dumps(value)
        return value
