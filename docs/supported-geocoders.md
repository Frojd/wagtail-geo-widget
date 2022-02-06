# Supported Geocoders

Geocoders are used by the address field (GeoAddressPanel/GeoAddressBlock) to enable searching for places in the map. We currently support these services:

## Nominatim

Url: [https://nominatim.org/](https://nominatim.org/)

### Example:

```python
from django.contrib.gis.db import models
from wagtail.core.models import Page
from wagtailgeowidget import geocoders
from wagtailgeowidget.blocks import GeoAddressPanel, LeafletPanel

class ExamplePage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoAddressPanel("address", geocoder=geocoders.NOMINATIM),
        LeafletPanel("location", address_field="address"),
    ]
```

## Google Maps Geocoding

Url: [https://developers.google.com/maps/documentation/javascript/geocoding](https://developers.google.com/maps/documentation/javascript/geocoding)

### Example:

```python
from django.contrib.gis.db import models
from wagtail.core.models import Page
from wagtailgeowidget import geocoders
from wagtailgeowidget.blocks import GeoAddressPanel, LeafletPanel

class ExamplePage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS),
        LeafletPanel("location", address_field="address"),
    ]
```
