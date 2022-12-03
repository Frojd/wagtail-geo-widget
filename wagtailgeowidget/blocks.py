from django import forms
from django.utils.functional import cached_property
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.blocks import FieldBlock, IntegerBlock
else:
    from wagtail.core.blocks import FieldBlock, IntegerBlock

from wagtailgeowidget import geocoders
from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtailgeowidget.widgets import GeocoderField, GoogleMapsField, LeafletField


class GeoAddressBlock(FieldBlock):
    class Meta:
        classname = "geo-address-block"

    def __init__(
        self,
        geocoder=geocoders.NOMINATIM,
        required=True,
        help_text=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.field_options = {
            "required": required,
            "help_text": help_text,
        }

        self.geocoder = geocoder

    @cached_property
    def field(self):
        field_kwargs = {
            "widget": GeocoderField(
                geocoder=self.geocoder,
            )
        }
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)


class GeoZoomBlock(IntegerBlock):
    class Meta:
        classname = "geo-zoom-block"


class GoogleMapsBlock(FieldBlock):
    class Meta:
        icon = "site"

    def __init__(
        self,
        address_field=None,
        zoom_field=None,
        required=True,
        help_text=None,
        hide_latlng=False,
        **kwargs,
    ):
        self.field_options = {}
        self.address_field = address_field
        self.zoom_field = zoom_field
        self.hide_latlng = hide_latlng

        super().__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {
            "widget": GoogleMapsField(
                srid=4326,
                id_prefix="",
                address_field=self.address_field,
                zoom_field=self.zoom_field,
                hide_latlng=self.hide_latlng,
            )
        }
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_form(self, value, prefix="", errors=None):
        if value and isinstance(value, dict):
            value = "SRID={};POINT({} {})".format(
                value["srid"],
                value["lng"],
                value["lat"],
            )

        return super().render_form(value, prefix, errors)

    def value_from_form(self, value):
        return value

    def value_for_form(self, value):
        if not value:
            return None

        if value and isinstance(value, str):
            return value

        val = "SRID={};POINT({} {})".format(
            4326,
            value["lng"],
            value["lat"],
        )
        return val

    def to_python(self, value):
        if isinstance(value, dict):
            return value

        value = geosgeometry_str_to_struct(value)
        value = {
            "lat": value["y"],
            "lng": value["x"],
            "srid": value["srid"],
        }

        return super().to_python(value)


class GeoBlock(GoogleMapsBlock):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            "GeoBlock will be deprecated in version 7, use GoogleMapsBlock instead",
            PendingDeprecationWarning,
        )

        super().__init__(*args, **kwargs)


class LeafletBlock(FieldBlock):
    class Meta:
        icon = "site"

    def __init__(
        self,
        address_field=None,
        zoom_field=None,
        required=True,
        help_text=None,
        hide_latlng=False,
        **kwargs,
    ):
        self.field_options = {}
        self.address_field = address_field
        self.zoom_field = zoom_field
        self.hide_latlng = hide_latlng
        super().__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {
            "widget": LeafletField(
                srid=4326,
                id_prefix="",
                address_field=self.address_field,
                zoom_field=self.zoom_field,
                hide_latlng=self.hide_latlng,
            )
        }
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_form(self, value, prefix="", errors=None):
        if value and isinstance(value, dict):
            value = "SRID={};POINT({} {})".format(
                value["srid"],
                value["lng"],
                value["lat"],
            )

        return super().render_form(value, prefix, errors)

    def value_from_form(self, value):
        return value

    def value_for_form(self, value):
        if not value:
            return None

        if value and isinstance(value, str):
            return value

        val = "SRID={};POINT({} {})".format(
            4326,
            value["lng"],
            value["lat"],
        )
        return val

    def to_python(self, value):
        if isinstance(value, dict):
            return value

        value = geosgeometry_str_to_struct(value)
        value = {
            "lat": value["y"],
            "lng": value["x"],
            "srid": value["srid"],
        }

        return super().to_python(value)
