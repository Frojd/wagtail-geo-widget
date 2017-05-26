from django.test import TestCase

from wagtailgeowidget.helpers import geosgeometry_str_to_struct


class LatLngTestCase(TestCase):
    def test_regular_coords(self):
        struct = geosgeometry_str_to_struct('SRID=5432;POINT(12.0 13.0)')
        self.assertEquals(struct['srid'], '5432')
        self.assertEquals(struct['x'], '12.0')
        self.assertEquals(struct['y'], '13.0')
