from django.test import SimpleTestCase

from wagtailgeowidget.helpers import geosgeometry_str_to_struct


class LatLngTestCase(SimpleTestCase):
    def test_regular_coords(self):
        struct = geosgeometry_str_to_struct("SRID=5432;POINT(12.0 13.0)")
        self.assertEqual(struct["srid"], "5432")
        self.assertEqual(struct["x"], "12.0")
        self.assertEqual(struct["y"], "13.0")

    def test_negative_coords(self):
        struct = geosgeometry_str_to_struct("SRID=5432;POINT(12.0 -13.0)")
        self.assertEqual(struct["srid"], "5432")
        self.assertEqual(struct["x"], "12.0")
        self.assertEqual(struct["y"], "-13.0")
