import unittest

from django.test import TestCase
from wagtail import VERSION as WAGTAIL_VERSION

from wagtailgeowidget import app_settings, geocoders
from wagtailgeowidget.widgets import (
    GeocoderField,
    GoogleMapsField,
    GoogleMapsFieldAdapter,
    LeafletField,
    LeafletFieldAdapter,
)


class GoogleMapsFieldTestCase(TestCase):
    def test_google_maps_field_contains_construct(self):
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

    def test_streamfield_widget_uses_empty_id_prefix(self):
        """Test that StreamField widgets use empty id_prefix."""

        widget = GoogleMapsField(srid=4326, id_prefix="")

        self.assertEqual(widget.id_prefix, "")

    def test_fieldpanel_widget_includes_stimulus_attributes(self):
        """Test that FieldPanel widgets (id_prefix='id_') include Stimulus controller attributes."""

        widget = GoogleMapsField(srid=4326, id_prefix="id_")
        html = widget.render(
            "field",
            "SRID=4326;POINT(18.0686 59.3293)",
            {
                "id": "test-field",
            },
        )

        self.assertIn('data-controller="google-maps-field"', html)
        self.assertIn("data-google-maps-field-options-value=", html)

    def test_streamfield_widget_excludes_stimulus_attributes(self):
        """Test that StreamField widgets (id_prefix='') exclude Stimulus controller attributes."""
        widget = GoogleMapsField(srid=4326, id_prefix="")

        html = widget.render(
            "field",
            "SRID=4326;POINT(18.0686 59.3293)",
            {
                "id": "test-field",
            },
        )

        self.assertNotIn('data-controller="google-maps-field"', html)
        self.assertNotIn("data-google-maps-field-options-value=", html)

    @unittest.skipIf(WAGTAIL_VERSION < (7, 1), "Test only applicable for Wagtail 7.1+")
    def test_telepath_adapter_js_args_structure(self):
        """Test that the adapter returns correct js_args structure for Telepath."""

        widget = GoogleMapsField(
            srid=4326,
            address_field="address",
            zoom_field="zoom",
        )
        adapter = GoogleMapsFieldAdapter()

        result = adapter.js_args(widget)

        self.assertEqual(len(result), 2)

        self.assertIsInstance(result[0], str)
        self.assertIn('<input type="hidden"', result[0])

        self.assertIsInstance(result[1], dict)
        options = result[1]

        self.assertIn("srid", options)
        self.assertIn("addressField", options)
        self.assertIn("zoomField", options)
        self.assertIn("defaultLocation", options)
        self.assertIn("zoom", options)
        self.assertIn("mapId", options)

        self.assertEqual(options["srid"], 4326)
        self.assertEqual(options["addressField"], "address")
        self.assertEqual(options["zoomField"], "zoom")

    def test_telepath_adapter_streamfield_excludes_stimulus_attributes(self):
        """Test that HTML by adapter for StreamField widget has no Stimulus attributes."""

        widget = GoogleMapsField(srid=4326, id_prefix="")
        adapter = GoogleMapsFieldAdapter()

        result = adapter.js_args(widget)
        html = result[0]

        self.assertNotIn("data-controller=", html)
        self.assertNotIn("data-google-maps-field-options-value=", html)


class LeafletFieldTestCase(TestCase):
    def test_leaflet_field_contains_construct(self):
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

    def test_streamfield_widget_uses_empty_id_prefix(self):
        """Test that StreamField widgets use empty id_prefix."""

        widget = LeafletField(srid=4326, id_prefix="")

        self.assertEqual(widget.id_prefix, "")

    def test_fieldpanel_widget_includes_stimulus_attributes(self):
        """Test that FieldPanel widgets (id_prefix='id_') include Stimulus controller attributes."""

        widget = LeafletField(srid=4326, id_prefix="id_")
        html = widget.render(
            "field",
            "SRID=4326;POINT(18.0686 59.3293)",
            {
                "id": "test-field",
            },
        )

        self.assertIn('data-controller="leaflet-field"', html)
        self.assertIn("data-leaflet-field-options-value=", html)

    def test_streamfield_widget_excludes_stimulus_attributes(self):
        """Test that StreamField widgets (id_prefix='') exclude Stimulus controller attributes."""

        widget = LeafletField(srid=4326, id_prefix="")

        html = widget.render(
            "field",
            "SRID=4326;POINT(18.0686 59.3293)",
            {
                "id": "test-field",
            },
        )

        self.assertNotIn('data-controller="leaflet-field"', html)
        self.assertNotIn("data-leaflet-field-options-value=", html)

    @unittest.skipIf(WAGTAIL_VERSION < (7, 1), "Test only applicable for Wagtail 7.1+")
    def test_telepath_adapter_js_args_structure(self):
        """Test that the adapter returns correct js_args structure for Telepath."""

        widget = LeafletField(
            srid=4326,
            address_field="address",
            zoom_field="zoom",
        )
        adapter = LeafletFieldAdapter()

        result = adapter.js_args(widget)

        self.assertEqual(len(result), 2)

        self.assertIsInstance(result[0], str)
        self.assertIn('<input type="hidden"', result[0])

        self.assertIsInstance(result[1], dict)
        options = result[1]

        self.assertIn("srid", options)
        self.assertIn("addressField", options)
        self.assertIn("zoomField", options)
        self.assertIn("defaultLocation", options)
        self.assertIn("zoom", options)

        self.assertEqual(options["srid"], 4326)
        self.assertEqual(options["addressField"], "address")
        self.assertEqual(options["zoomField"], "zoom")

    def test_telepath_adapter_streamfield_excludes_stimulus_attributes(self):
        """Test that HTML by adapter for StreamField widget has no Stimulus attributes."""

        widget = LeafletField(srid=4326, id_prefix="")
        adapter = LeafletFieldAdapter()

        result = adapter.js_args(widget)
        html = result[0]

        self.assertNotIn("data-controller=", html)
        self.assertNotIn("data-leaflet-field-options-value=", html)


class GeocoderFieldTestCase(TestCase):
    def setUp(self):
        app_settings.MAPBOX_ACCESS_TOKEN = None
        app_settings.MAPBOX_LANGUAGE = "en"

    def test_geocoder_field_contains_construct(self):
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
