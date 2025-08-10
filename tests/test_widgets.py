from django.test import TestCase

from wagtailgeowidget import app_settings, geocoders
from wagtailgeowidget.widgets import GeocoderField, GoogleMapsField, LeafletField


class GoogleMapsFieldTestCase(TestCase):
    def test_google_maps_field_contains_constuct(self):
        widget = GoogleMapsField()
        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )

        self.assertIn(
            '<input type="hidden" name="field" id="X" data-controller="google-maps-field"',
            html,
        )


class LeafletFieldTestCase(TestCase):
    def test_leaflet_field_contains_constuct(self):
        widget = LeafletField()
        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )

        self.assertIn(
            '<input type="hidden" name="field" id="X" data-controller="leaflet-field"',
            html,
        )

    def test_leaflet_field_js_init_contains_construct(self):
        widget = LeafletField()

        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )
        self.assertIn(
            '<input type="hidden" name="field" id="X" data-controller="leaflet-field"',
            html,
        )

    def test_value_are_parsed_properly(self):
        widget = LeafletField()

        from html import escape

        html = widget.render(
            "field",
            "SRID=5432;POINT(12.0 13.0)",
            {
                "id": "X",
            },
        )
        self.assertIn(escape('"lat": "13.0"'), html)
        self.assertIn(escape('"lng": "12.0"'), html)


class GeocoderFieldTestCase(TestCase):
    def setUp(self):
        app_settings.MAPBOX_ACCESS_TOKEN = None
        app_settings.MAPBOX_LANGUAGE = "en"

    def test_geocoder_field_contains_constuct(self):
        widget = GeocoderField()
        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )

        self.assertIn(
            '<input type="text" name="field" id="X" data-controller="geocoder-field" data-geocoder-field-geocoder-value="nominatim"',
            html,
        )

    def test_googlemaps_geocoder_returns_googlemaps_field(self):
        widget = GeocoderField(geocoder=geocoders.GOOGLE_MAPS)

        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )
        self.assertIn(
            '<input type="text" name="field" id="X" data-controller="geocoder-field" data-geocoder-field-geocoder-value="google_maps"',
            html,
        )

    def test_googlemaps_places_geocoder_returns_googlemaps_field(self):
        widget = GeocoderField(geocoder=geocoders.GOOGLE_MAPS_PLACES)

        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )
        self.assertIn(
            '<input type="text" name="field" id="X" data-controller="geocoder-field" data-geocoder-field-geocoder-value="google_maps_places"',
            html,
        )

    def test_googlemaps_places_new_geocoder_returns_googlemaps_field(self):
        widget = GeocoderField(geocoder=geocoders.GOOGLE_MAPS_PLACES_NEW)

        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )
        self.assertIn(
            '<input type="text" name="field" id="X" data-controller="geocoder-field" data-geocoder-field-geocoder-value="google_maps_places_new"',
            html,
        )

    def test_mapbox_geocoder_returns_googlemaps_field(self):
        widget = GeocoderField(geocoder=geocoders.MAPBOX)

        from html import escape

        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )
        self.assertIn(
            '<input type="text" name="field" id="X" data-controller="geocoder-field" data-geocoder-field-geocoder-value="mapbox"',
            html,
        )
        self.assertIn(escape('accessToken": null'), html)

    def test_mapbox_access_token_gets_outputted(self):
        app_settings.MAPBOX_ACCESS_TOKEN = "<MAPBOX ACCESS TOKEN>"

        widget = GeocoderField(geocoder=geocoders.MAPBOX)

        from html import escape

        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )
        self.assertIn(
            '<input type="text" name="field" id="X" data-controller="geocoder-field" data-geocoder-field-geocoder-value="mapbox"',
            html,
        )
        self.assertIn(escape('accessToken": "<MAPBOX ACCESS TOKEN>'), html)

        app_settings.MAPBOX_ACCESS_TOKEN = None

    def test_mapbox_language_parameter_gets_outputted(self):
        widget = GeocoderField(geocoder=geocoders.MAPBOX)

        from html import escape

        html = widget.render(
            "field",
            "",
            {
                "id": "X",
            },
        )
        self.assertIn(
            '<input type="text" name="field" id="X" data-controller="geocoder-field" data-geocoder-field-geocoder-value="mapbox"',
            html,
        )
        self.assertIn(escape('language": "en'), html)
