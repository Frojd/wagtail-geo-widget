import json

from django import forms
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.safestring import mark_safe

try:
    from django.contrib.gis.geos.point import Point
except:  # NOQA
    Point = None

from wagtailgeowidget.app_settings import (
    GEO_WIDGET_DEFAULT_LOCATION,
    GEO_WIDGET_EMPTY_LOCATION,
    GEO_WIDGET_ZOOM,
)
from wagtailgeowidget.helpers import geosgeometry_str_to_struct


class GeoField(forms.HiddenInput):
    address_field = None
    zoom_field = None
    id_prefix = "id_"
    srid = None
    hide_latlng = False
    used_in = "GeoField"

    def __init__(self, *args, **kwargs):
        self.address_field = kwargs.pop("address_field", self.address_field)
        self.zoom_field = kwargs.pop("zoom_field", self.zoom_field)
        self.srid = kwargs.pop("srid", self.srid)
        self.hide_latlng = kwargs.pop("hide_latlng", self.hide_latlng)
        self.id_prefix = kwargs.pop("id_prefix", self.id_prefix)
        self.zoom = kwargs.pop("zoom", GEO_WIDGET_ZOOM)
        self.used_in = kwargs.pop("used_in", "GeoField")

        super(GeoField, self).__init__(*args, **kwargs)

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
            css={"all": ("wagtailgeowidget/css/geo-field.css",)},
            js=(
                "wagtailgeowidget/js/geo-field.js",
                "https://maps.google.com/maps/api/js?key={}&libraries=places&language={}".format(
                    google_maps_apikey,
                    GOOGLE_MAPS_V3_LANGUAGE,
                ),
            ),
        )

    def render(self, name, value, attrs=None, renderer=None):
        out = super(GeoField, self).render(name, value, attrs, renderer=renderer)

        input_classes = "geo-field-location"
        if self.hide_latlng:
            input_classes = "{} {}".format(
                input_classes,
                "geo-field-location--hide",
            )

        location = format_html(
            '<div class="input">'
            '<input id="_id_{}_latlng" class="{}" maxlength="250" type="text">'
            "</div>",
            name,
            input_classes,
        )

        in_react_streamfield = (
            # if wagtail 2.13+ streamfield
            attrs.get("id", "").endswith("__ID__")
            or
            # if wagtail-react-streamfield
            name.endswith("__ID__")
        )

        namespace = ""
        if "-" in name:
            namespace = name.split("-")[:-1]
            namespace = "-".join(namespace)
            namespace = "{}-".format(namespace)

        source_selector = "#{}{}".format(self.id_prefix, name)
        address_selector = "#{}{}{}".format(
            self.id_prefix,
            namespace,
            self.address_field,
        )
        zoom_selector = "#{}{}{}".format(
            self.id_prefix,
            namespace,
            self.zoom_field,
        )

        data = {
            "sourceSelector": source_selector,
            "defaultLocation": GEO_WIDGET_DEFAULT_LOCATION,
            "addressSelector": address_selector,
            "zoomSelector": zoom_selector,
            "latLngDisplaySelector": "#_id_{}_latlng".format(name),
            "zoom": self.zoom,
            "srid": self.srid,
            "usedIn": self.used_in,
            "inReactStreamfield": in_react_streamfield,
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

        # If a value is set we should show the map independent
        # of what GEO_WIDGET_EMPTY_LOCATION is set to.
        if not value and GEO_WIDGET_EMPTY_LOCATION:
            data["showEmptyLocation"] = True

        json_data = json.dumps(data)
        data_id = "geo_field_{}_data".format(name)

        return mark_safe(
            '<script>window["{}"] = {};</script>'.format(data_id, json_data)
            + out
            + location
            + '<div class="geo-field" data-data-id="{}"></div>'.format(data_id)
            + """
            <script>
            (function(){
                if (document.readyState === 'complete') {
                    return initializeGeoFields();
                }

                $(window).on('load', function() {
                    initializeGeoFields();
                });
            })();
            </script>
            """
        )
