import json

from django import forms
from django.forms import widgets
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from wagtail.core.telepath import register
from wagtail.core.widget_adapters import WidgetAdapter
from wagtail.utils.widgets import WidgetWithScript

try:
    from django.contrib.gis.geos.point import Point
except:  # NOQA
    Point = None

from wagtailgeowidget import geocoders
from wagtailgeowidget.app_settings import (
    GEO_WIDGET_DEFAULT_LOCATION,
    GEO_WIDGET_EMPTY_LOCATION,
    GEO_WIDGET_LEAFLET_TILE_LAYER,
    GEO_WIDGET_LEAFLET_TILE_LAYER_OPTIONS,
    GEO_WIDGET_ZOOM,
)
from wagtailgeowidget.helpers import geosgeometry_str_to_struct


class GoogleMapsField(WidgetWithScript, forms.HiddenInput):
    address_field = None
    zoom_field = None
    id_prefix = "id_"
    srid = None
    hide_latlng = False

    def __init__(self, *args, **kwargs):
        self.address_field = kwargs.pop("address_field", self.address_field)
        self.zoom_field = kwargs.pop("zoom_field", self.zoom_field)
        self.srid = kwargs.pop("srid", self.srid)
        self.hide_latlng = kwargs.pop("hide_latlng", self.hide_latlng)
        self.id_prefix = kwargs.pop("id_prefix", self.id_prefix)
        self.zoom = kwargs.pop("zoom", GEO_WIDGET_ZOOM)

        super().__init__(*args, **kwargs)

    @cached_property
    def media(self):
        from django.utils.module_loading import import_string

        from wagtailgeowidget.app_settings import (
            GOOGLE_MAPS_V3_APIKEY,
            GOOGLE_MAPS_V3_APIKEY_CALLBACK,
            GOOGLE_MAPS_V3_LANGUAGE,
        )

        google_maps_apikey = GOOGLE_MAPS_V3_APIKEY

        if GOOGLE_MAPS_V3_APIKEY_CALLBACK:
            if isinstance(GOOGLE_MAPS_V3_APIKEY_CALLBACK, str):
                callback = import_string(GOOGLE_MAPS_V3_APIKEY_CALLBACK)
            else:
                callback = GOOGLE_MAPS_V3_APIKEY_CALLBACK

            google_maps_apikey = callback()

        return forms.Media(
            css={"all": ("wagtailgeowidget/css/google-maps-field.css",)},
            js=(
                "wagtailgeowidget/js/google-maps-field.js",
                "https://maps.google.com/maps/api/js?key={}&libraries=places&language={}".format(
                    google_maps_apikey,
                    GOOGLE_MAPS_V3_LANGUAGE,
                ),
            ),
        )

    def render_js_init(self, id_, name, value):
        input_classes = "google-maps-field-location"
        if self.hide_latlng:
            input_classes = "{} {}".format(
                input_classes,
                "google-maps-field-location--hide",
            )

        location = format_html(
            '<div class="input">'
            '<input id="_id_{}_latlng" class="{}" maxlength="250" type="text">'
            "</div>",
            name,
            input_classes,
        )

        source_selector = "#{}{}".format(self.id_prefix, name)
        address_selector = "#{}{}".format(
            self.id_prefix,
            self.address_field,
        )
        zoom_selector = "#{}{}".format(
            self.id_prefix,
            self.zoom_field,
        )

        data = {
            "defaultLocation": GEO_WIDGET_DEFAULT_LOCATION,
            "addressSelector": address_selector,
            "zoomSelector": zoom_selector,
            "zoom": self.zoom,
            "srid": self.srid,
        }

        if value and isinstance(value, str):
            result = geosgeometry_str_to_struct(value)
            if result:
                data["defaultLocation"] = {
                    "lat": result["y"],
                    "lng": result["x"],
                }

        if value and Point and isinstance(value, Point):
            data["defaultLocation"] = {
                "lat": value.y,
                "lng": value.x,
            }

        return "new GoogleMapsField({0});".format(
            json.dumps(
                {
                    "id": id_,
                    **data,
                }
            ),
        )

    def render(self, name, value, attrs=None, renderer=None):
        try:
            id_ = attrs["id"]
        except (KeyError, TypeError):
            raise TypeError(
                "WidgetWithScript cannot be rendered without an 'id' attribute"
            )

        value_data = self.get_value_data(value)
        widget_html = self.render_html(name, value_data, attrs)

        input_classes = "google-maps-location"
        location = format_html(
            '<div class="input">'
            '<input id="{0}_latlng" class="{1}" maxlength="250" type="text">'
            "</div>",
            id_,
            input_classes,
        )

        js = self.render_js_init(id_, name, value_data)
        return mark_safe(
            widget_html
            + location
            + '<div id="{0}_map" class="google-maps-field"></div>'.format(id_)
            + "<script>{0}</script>".format(js)
        )


class GoogleMapsFieldAdapter(WidgetAdapter):
    js_constructor = "wagtailgewidget.widgets.GoogleMapsFieldAdapter"

    def js_args(self, widget):
        args = super().js_args(widget)

        return [
            *args,
            {
                "addressField": widget.address_field,
                "zoomField": widget.zoom_field,
                "defaultLocation": GEO_WIDGET_DEFAULT_LOCATION,
                "srid": widget.srid,
                "zoom": widget.zoom,
            },
        ]

    class Media:
        js = ["wagtailgeowidget/js/google-maps-field-telepath.js"]


register(GoogleMapsFieldAdapter(), GoogleMapsField)


class GeoField(GoogleMapsField):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            "GeoField will be deprecated in version 7, use GoogleMapsField instead",
            PendingDeprecationWarning,
        )

        super().__init__(*args, **kwargs)


# class GeocoderField(forms.HiddenInput):
class GeocoderField(WidgetWithScript, widgets.TextInput):
    geocoder = None

    def __init__(self, *args, **kwargs):
        self.geocoder = kwargs.pop("geocoder", geocoders.NOMINATIM)

        super().__init__(*args, **kwargs)

    @property
    def media(self):
        js = ["wagtailgeowidget/js/geocoder-field.js"]

        from wagtailgeowidget.app_settings import (
            GOOGLE_MAPS_V3_APIKEY,
            GOOGLE_MAPS_V3_LANGUAGE,
        )

        if self.geocoder == geocoders.GOOGLE_MAPS:
            js = [
                *js,
                "https://maps.google.com/maps/api/js?key={}&libraries=places&language={}".format(
                    GOOGLE_MAPS_V3_APIKEY,
                    GOOGLE_MAPS_V3_LANGUAGE,
                ),
            ]

        return forms.Media(
            js=js,
        )

    def render_js_init(self, id_, name, value):
        field_by_geocoder = {
            "nominatim": "NominatimGeocoderField",
            "google_maps": "GoogleMapsGeocoderField",
        }

        return "new {0}({1});".format(
            field_by_geocoder[self.geocoder],
            json.dumps({"id": id_}),
        )


class GeocoderFieldAdapter(WidgetAdapter):
    js_constructor = "wagtailgewidget.widgets.GeocoderFieldWrap"

    def js_args(self, widget):
        args = super().js_args(widget)
        return [*args, widget.geocoder]

    class Media:
        js = ["wagtailgeowidget/js/geocoder-field-telepath.js"]


register(GeocoderFieldAdapter(), GeocoderField)


class LeafletField(WidgetWithScript, forms.HiddenInput):
    address_field = None
    zoom_field = None
    id_prefix = "id_"
    srid = None
    hide_latlng = False

    def __init__(self, *args, **kwargs):
        self.address_field = kwargs.pop("address_field", self.address_field)
        self.zoom_field = kwargs.pop("zoom_field", self.zoom_field)
        self.srid = kwargs.pop("srid", self.srid)
        self.hide_latlng = kwargs.pop("hide_latlng", self.hide_latlng)
        self.id_prefix = kwargs.pop("id_prefix", self.id_prefix)
        self.zoom = kwargs.pop("zoom", GEO_WIDGET_ZOOM)

        super().__init__(*args, **kwargs)

    @cached_property
    def media(self):
        return forms.Media(
            css={
                "all": (
                    "wagtailgeowidget/css/leaflet-field.css",
                    "https://unpkg.com/leaflet@1.7.1/dist/leaflet.css",
                )
            },
            js=(
                "wagtailgeowidget/js/leaflet-field.js",
                "https://unpkg.com/leaflet@1.7.1/dist/leaflet.js",
            ),
        )

    def render_js_init(self, id_, name, value):
        input_classes = "leaflet-field-location"
        if self.hide_latlng:
            input_classes = "{} {}".format(
                input_classes,
                "leaflet-field-location--hide",
            )

        location = format_html(
            '<div class="input">'
            '<input id="_id_{}_latlng" class="{}" maxlength="250" type="text">'
            "</div>",
            name,
            input_classes,
        )

        source_selector = "#{}{}".format(self.id_prefix, name)
        address_selector = "#{}{}".format(
            self.id_prefix,
            self.address_field,
        )
        zoom_selector = "#{}{}".format(
            self.id_prefix,
            self.zoom_field,
        )

        data = {
            "defaultLocation": GEO_WIDGET_DEFAULT_LOCATION,
            "addressSelector": address_selector,
            "zoomSelector": zoom_selector,
            "zoom": self.zoom,
            "srid": self.srid,
            "tileLayer": GEO_WIDGET_LEAFLET_TILE_LAYER,
            "tileLayerOptions": GEO_WIDGET_LEAFLET_TILE_LAYER_OPTIONS,
        }

        if value and isinstance(value, str):
            result = geosgeometry_str_to_struct(value)
            if result:
                data["defaultLocation"] = {
                    "lat": result["y"],
                    "lng": result["x"],
                }

        if value and Point and isinstance(value, Point):
            data["defaultLocation"] = {
                "lat": value.y,
                "lng": value.x,
            }

        return "new LeafletField({0});".format(
            json.dumps(
                {
                    "id": id_,
                    **data,
                }
            ),
        )

    def render(self, name, value, attrs=None, renderer=None):
        try:
            id_ = attrs["id"]
        except (KeyError, TypeError):
            raise TypeError(
                "WidgetWithScript cannot be rendered without an 'id' attribute"
            )

        value_data = self.get_value_data(value)
        widget_html = self.render_html(name, value_data, attrs)

        input_classes = "leaflet-field-location"
        location = format_html(
            '<div class="input">'
            '<input id="{0}_latlng" class="{1}" maxlength="250" type="text">'
            "</div>",
            id_,
            input_classes,
        )

        js = self.render_js_init(id_, name, value_data)
        return mark_safe(
            widget_html
            + location
            + '<div id="{0}_map" class="leaflet-field"></div>'.format(id_)
            + "<script>{0}</script>".format(js)
        )


class LeafletFieldAdapter(WidgetAdapter):
    js_constructor = "wagtailgewidget.widgets.LeafletFieldAdapter"

    def js_args(self, widget):
        args = super().js_args(widget)

        return [
            *args,
            {
                "addressField": widget.address_field,
                "zoomField": widget.zoom_field,
                "defaultLocation": GEO_WIDGET_DEFAULT_LOCATION,
                "srid": widget.srid,
                "zoom": widget.zoom,
                "tileLayer": GEO_WIDGET_LEAFLET_TILE_LAYER,
                "tileLayerOptions": GEO_WIDGET_LEAFLET_TILE_LAYER_OPTIONS,
            },
        ]

    class Media:
        js = ["wagtailgeowidget/js/leaflet-field-telepath.js"]


register(LeafletFieldAdapter(), LeafletField)
