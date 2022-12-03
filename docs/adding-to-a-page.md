# Adding Wagtail-Geo-Widget to a Page

This documents explains how to add a Google Maps map to pages in various ways.

If you instead want to use Leaflet, just change `GoogleMapsPanel` to `LeafletPanel`

### First create a page

```python
from wagtail.models import Page

class MyPage(Page):
    ...
```


### Create a CharField that represents your data

Define a CharField representing your location, in this example we call it `location`.

```python
from django.db import models
from wagtail.models import Page

class MyPage(Page):
    location = models.CharField(max_length=250, blank=True, null=True)
```


### Add a content panel to represent the field in the admin

```python
from django.db import models
from wagtail.models import Page
from wagtailgeowidget.panels import GoogleMapsPanel


class MyPage(Page):
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        GoogleMapsPanel('location'),
    ]
```


### The format of your location

When you update your page in the admin and add a location you will notice that the address will be stored as a `GEOSGeometry` string in the database (Example: `SRID=4326;POINT(17.35448867187506 59.929179873751934)`.

It is a excellent format because this allows us to use the same GoogleMapsPanel for both the spatial field and a non-spatial field, but nothing we can display to our users. So lets add a helper that parses this into lat/lng.


```python
from django.utils.functional import cached_property
from wagtail.models import Page
from wagtailgeowidget.helpers import geosgeometry_str_to_struct

class MyPage(Page):
    # ...

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point['y']

    @property
    def lng(self):
        return self.point['x']
```

With the helpers if place, you call `lat` or `lng` to access the coordinates.


### Adding an address field

With the address field users can search for a location that will be shown in the map. This is a process called geocoding, where we transform a description of a place to a location.

The address field supports several different geocoding services, but in this example below we use the Google Maps Geocoding service. You change the geocoder service by changing the geocoder param.

The address field are optional and needs to be added separately, the panel accepts an `address_field` if you want to use the map in coordination with a geo-lookup (like the screenshot on top).


```python
from django.db import models
from django.utils.translation import gettext as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtailgeowidget import geocoders
from wagtailgeowidget.panels import GeoAddressPanel, GoogleMapsPanel


class MyPageWithAddressField(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS),
            GoogleMapsPanel('location', address_field='address'),
        ], _('Geo details')),
    ]
```


### Adding an zoom field

The zoom field works in a similar way as the address field and needs to be added separately, the panel accepts an `zoom_field` where the map zoom state is written to this field. The zoom field can be used in conjunction with the address field.


```python
from django.db import models
from django.utils.translation import gettext as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtailgeowidget.panels import GoogleMapsPanel


class MyPageWithZoomField(Page):
    zoom = models.SmallIntegerField(blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("zoom"),
            GoogleMapsPanel("location", zoom_field="zoom"),
        ], _('Geo details')),
    ]
```


### More examples

For more examples, look at the [example](https://github.com/Frojd/wagtail-geo-widget/blob/develop/tests/geopage/models.py).
