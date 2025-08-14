import json
import uuid

from django import forms
from django.forms import widgets
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (7, 1):
    from wagtail.admin.telepath import register
    from wagtail.admin.telepath.widgets import WidgetAdapter
else:
    from wagtail.telepath import register
    from wagtail.widget_adapters import WidgetAdapter

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

translations = {
    "error_message_invalid_location": _(
        "Invalid location coordinate, use Latitude and Longitude (example: 59.329,18.06858)"
    ),
    "success_address_geocoded": _("Address has been successfully geo-coded"),
    "error_could_not_geocode_address": _(
        "Could not geocode address '%s'. The map may not be in sync with the address entered."
    ),
    "enter_location": _("Enter a location"),
    "initialize_map": _("Click here to initialize map"),
}


class GoogleMapsField(forms.HiddenInput):
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
        self.map_id = str(uuid.uuid4())

        # Keeps a reference to the value data from the render method
        self.value_data = None

        super().__init__(*args, **kwargs)

    def build_attrs(self, *args, **kwargs):
        data = {
            "defaultLocation": GEO_WIDGET_DEFAULT_LOCATION,
            "addressField": self.address_field,
            "zoomField": self.zoom_field,
            "zoom": self.zoom,
            "srid": self.srid,
            "showEmptyLocation": GEO_WIDGET_EMPTY_LOCATION,
            "translations": translations,
            "mapId": self.map_id,
        }

        if self.value_data and isinstance(self.value_data, str):
            result = geosgeometry_str_to_struct(self.value_data)
            if result:
                data["defaultLocation"] = {
                    "lat": result["y"],
                    "lng": result["x"],
                }

        if self.value_data and Point and isinstance(self.value_data, Point):
            data["defaultLocation"] = {
                "lat": self.value_data.y,
                "lng": self.value_data.x,
            }

        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "google-maps-field"
        attrs["data-google-maps-field-options-value"] = json.dumps(data)
        return attrs

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
                "wagtailgeowidget/js/google-maps-field-controller.js",
                "https://maps.google.com/maps/api/js?key={}&libraries=places,marker&language={}".format(
                    google_maps_apikey,
                    GOOGLE_MAPS_V3_LANGUAGE,
                ),
            ),
        )

    def render(self, name, value, attrs=None, renderer=None):
        try:
            id_ = attrs["id"]
        except (KeyError, TypeError):
            raise TypeError(
                "GoogleMapsField cannot be rendered without an 'id' attribute"
            )

        self.value_data = value
        widget_html = super().render(name, self.value_data, attrs)

        input_classes = "google-maps-location"
        if self.hide_latlng:
            input_classes = "{} {}".format(
                input_classes,
                "google-maps-field-location--hide",
            )

        location = format_html(
            '<div class="input">'
            '<input id="{0}_latlng" class="{1}" maxlength="250" type="text">'
            "</div>",
            id_,
            input_classes,
        )

        return mark_safe(
            widget_html
            + location
            + '<div id="{0}_map" class="google-maps-field"></div>'.format(id_)
        )


class GeocoderField(widgets.TextInput):
    geocoder = geocoders.NOMINATIM

    def __init__(self, *args, **kwargs):
        self.geocoder = kwargs.pop("geocoder", geocoders.NOMINATIM)

        super().__init__(*args, **kwargs)

    def build_attrs(self, *args, **kwargs):
        options = {"translations": translations}
        params = {}
        if self.geocoder == geocoders.MAPBOX:
            from wagtailgeowidget.app_settings import (
                MAPBOX_ACCESS_TOKEN,
                MAPBOX_LANGUAGE,
            )

            params["accessToken"] = MAPBOX_ACCESS_TOKEN
            params["language"] = MAPBOX_LANGUAGE

        options["params"] = params

        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "geocoder-field"
        attrs["data-geocoder-field-geocoder-value"] = self.geocoder
        attrs["data-geocoder-field-options-value"] = json.dumps(options)
        return attrs

    @property
    def media(self):
        js = [
            "wagtailgeowidget/js/geocoder-field.js",
            "wagtailgeowidget/js/geocoder-field-controller.js",
        ]

        from wagtailgeowidget.app_settings import (
            GOOGLE_MAPS_V3_APIKEY,
            GOOGLE_MAPS_V3_LANGUAGE,
        )

        if self.geocoder == geocoders.GOOGLE_MAPS:
            js = [
                *js,
                "https://maps.google.com/maps/api/js?key={}&libraries=places,marker&language={}".format(
                    GOOGLE_MAPS_V3_APIKEY,
                    GOOGLE_MAPS_V3_LANGUAGE,
                ),
            ]

        return forms.Media(
            js=js,
        )

    def render(self, name, value, attrs=None, renderer=None):
        try:
            attrs["id"]
        except (KeyError, TypeError):
            raise TypeError(
                "GeocoderField cannot be rendered without an 'id' attribute"
            )

        value_data = value
        widget_html = super().render(name, value_data, attrs)

        return mark_safe(widget_html)


class LeafletField(forms.HiddenInput):
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

        # Keeps a reference to the value data from the render method
        self.value_data = None

        super().__init__(*args, **kwargs)

    def build_attrs(self, *args, **kwargs):
        data = {
            "defaultLocation": GEO_WIDGET_DEFAULT_LOCATION,
            "addressField": self.address_field,
            "zoomField": self.zoom_field,
            "zoom": self.zoom,
            "srid": self.srid,
            "tileLayer": GEO_WIDGET_LEAFLET_TILE_LAYER,
            "tileLayerOptions": GEO_WIDGET_LEAFLET_TILE_LAYER_OPTIONS,
            "showEmptyLocation": GEO_WIDGET_EMPTY_LOCATION,
            "translations": translations,
        }

        if self.value_data and isinstance(self.value_data, str):
            result = geosgeometry_str_to_struct(self.value_data)
            if result:
                data["defaultLocation"] = {
                    "lat": result["y"],
                    "lng": result["x"],
                }

        if self.value_data and Point and isinstance(self.value_data, Point):
            data["defaultLocation"] = {
                "lat": self.value_data.y,
                "lng": self.value_data.x,
            }

        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "leaflet-field"
        attrs["data-leaflet-field-options-value"] = json.dumps(data)
        return attrs

    @cached_property
    def media(self):
        return forms.Media(
            css={
                "all": (
                    "wagtailgeowidget/css/leaflet-field.css",
                    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
                )
            },
            js=(
                "wagtailgeowidget/js/leaflet-field.js",
                "wagtailgeowidget/js/leaflet-field-controller.js",
                "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
            ),
        )

    def render(self, name, value, attrs=None, renderer=None):
        try:
            id_ = attrs["id"]
        except (KeyError, TypeError):
            raise TypeError("LeafletField cannot be rendered without an 'id' attribute")

        self.value_data = value
        widget_html = super().render(name, self.value_data, attrs)

        input_classes = "leaflet-field-location"
        if self.hide_latlng:
            input_classes = "{} {}".format(
                input_classes,
                "leaflet-field-location--hide",
            )

        location = format_html(
            '<div class="input">'
            '<input id="{0}_latlng" class="{1}" maxlength="250" type="text">'
            "</div>",
            id_,
            input_classes,
        )

        return mark_safe(
            widget_html
            + location
            + '<div id="{0}_map" class="leaflet-field"></div>'.format(id_)
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
                "showEmptyLocation": GEO_WIDGET_EMPTY_LOCATION,
                "translations": translations,
                "mapId": widget.map_id,
            },
        ]

    class Media:
        js = ["wagtailgeowidget/js/google-maps-field-telepath.js"]


register(GoogleMapsFieldAdapter(), GoogleMapsField)


class GeocoderFieldAdapter(WidgetAdapter):
    js_constructor = "wagtailgewidget.widgets.GeocoderFieldWrap"

    def js_args(self, widget):
        args = super().js_args(widget)

        params = {}

        if widget.geocoder == geocoders.MAPBOX:
            from wagtailgeowidget.app_settings import MAPBOX_ACCESS_TOKEN

            params["accessToken"] = MAPBOX_ACCESS_TOKEN

        return [*args, widget.geocoder, translations, params]

    class Media:
        js = ["wagtailgeowidget/js/geocoder-field-telepath.js"]


register(GeocoderFieldAdapter(), GeocoderField)


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
                "showEmptyLocation": GEO_WIDGET_EMPTY_LOCATION,
                "translations": translations,
            },
        ]

    class Media:
        js = ["wagtailgeowidget/js/leaflet-field-telepath.js"]


register(LeafletFieldAdapter(), LeafletField)
