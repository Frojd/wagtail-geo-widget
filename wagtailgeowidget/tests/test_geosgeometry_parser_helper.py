from django.test import SimpleTestCase

from wagtailgeowidget.helpers import geosgeometry_str_to_struct


class GeosGeometryPrserHelperTestCase(SimpleTestCase):
    def test_that_basic_parsing_works(self):
        struct = geosgeometry_str_to_struct("SRID=5432;POINT(12.0 13.0)")

        self.assertEqual(struct["srid"], "5432")
        self.assertEqual(struct["x"], "12.0")
        self.assertEqual(struct["y"], "13.0")

    def test_none_is_returned_on_invalid_struct(self):
        struct = geosgeometry_str_to_struct("S=5432_P(12.0 13.0)")

        self.assertEqual(struct, None)

    def test_that_optional_space_between_point_and_data_is_accepted(self):
        struct = geosgeometry_str_to_struct("SRID=5432;POINT (12.0 13.0)")

        self.assertEqual(struct["srid"], "5432")
        self.assertEqual(struct["x"], "12.0")
        self.assertEqual(struct["y"], "13.0")
