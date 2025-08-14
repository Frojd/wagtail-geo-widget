# Supported Geocoders

Geocoders are used by the address field (GeoAddressPanel/GeoAddressBlock) to enable searching for places in the map. We currently support these services:

## Nominatim

Url: [https://nominatim.org/](https://nominatim.org/)
Geocoder: `NOMINATIM`

### Example:

```python
from django.contrib.gis.db import models
from wagtail.models import Page
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
Geocoder: `GOOGLE_MAPS`

### Example:

```python
from django.contrib.gis.db import models
from wagtail.models import Page
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

## Google Maps Geocoding With Places

Url: [https://developers.google.com/maps/documentation/javascript/geocoding](https://developers.google.com/maps/documentation/javascript/geocoding) and [https://developers.google.com/maps/documentation/places/web-service/overview](https://developers.google.com/maps/documentation/places/web-service/overview)
Geocoder: `GOOGLE_MAPS_PLACES`
Description: Uses Google Maps geocoding with the deprecated Autocomplete widget

### Example:

```python
from django.contrib.gis.db import models
from wagtail.models import Page
from wagtailgeowidget import geocoders
from wagtailgeowidget.blocks import GeoAddressPanel, LeafletPanel

class ExamplePage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS_PLACES),
        LeafletPanel("location", address_field="address"),
    ]
```

## Google Maps Geocoding With Places (New)

Url: [https://developers.google.com/maps/documentation/javascript/geocoding](https://developers.google.com/maps/documentation/javascript/geocoding) and [https://developers.google.com/maps/documentation/places/web-service/op-overview](https://developers.google.com/maps/documentation/places/web-service/op-overview)
Geocoder: `GOOGLE_MAPS_PLACES_NEW`
Description: Uses Google Maps geocoding with the Places New API and the AutocompleteElement

### Example:

```python
from django.contrib.gis.db import models
from wagtail.models import Page
from wagtailgeowidget import geocoders
from wagtailgeowidget.blocks import GeoAddressPanel, LeafletPanel

class ExamplePage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS_PLACES_NEW),
        LeafletPanel("location", address_field="address"),
    ]
```


## Mapbox

Url: [https://docs.mapbox.com/api/search/geocoding/](https://docs.mapbox.com/api/search/geocoding/)

### Example:

```python
from django.contrib.gis.db import models
from wagtail.models import Page
from wagtailgeowidget import geocoders
from wagtailgeowidget.blocks import GeoAddressPanel, LeafletPanel

class ExamplePage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoAddressPanel("address", geocoder=geocoders.MAPBOX),
        LeafletPanel("location", address_field="address"),
    ]
```
