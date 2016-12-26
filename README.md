[![PyPI version](https://badge.fury.io/py/wagtailgeowidget.svg)](https://badge.fury.io/py/wagtailgeowidget)

# Wagtail-Geo-Widget

A Google Maps widget for the GeoDjango PointField field in Wagtail.

![Screen1](https://raw.githubusercontent.com/frojd/wagtail-geo-widget/develop/img/screen1.png)


## Requirements

- Python 2.7 / Python 3.5
- Wagtail 1.7+ and Django (with GeoDjango)


## Installation

Install the library with pip:

```
$ pip install wagtailgeowidget
```


## Quick Setup

Make sure wagtail_geo_widget is added to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = (
    # ...
    'wagtailgeowidget',
)

```

Obtain a Google Maps API key and add it to your django settings `GOOGLE_MAPS_V3_APIKEY`

This should be enough to get started.


## Usage

### Without address field

First make sure you have a location field defined in your model, then add a GeoPanel among your content_panels.

```python
from django.contrib.gis.db import models
from wagtailgeowidget.edit_handlers import GeoPanel


class MyPage(Page):
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoPanel('location'),
    ]
```


### With a address field

The panel accepts a `address_field` if you want to the map in coordiation with a geo-lookup (like the screenshot on top).


```python
from django.contrib.gis.db import models
from wagtailgeowidget.edit_handlers import GeoPanel


class MyPageWithAddressField(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoPanel('location', address_field='address'),
    ]
```


## Settings

- `GOOGLE_MAPS_V3_APIKEY`: Api key for google maps (required).
- `GEO_WIDGET_DEFAULT_LOCATION`: Default map location when no coordinates are set, accepts a dict with lat and lng keys (required, default is `{'lat': 59.3293, 'lng': 18.0686}` that is Stockholm/Sweden).
- `GEO_WIDGET_ZOOM`: Default zoom level for map (required, 7 is default).


## Roadmap

- [x] Editable map widget for GeoDjango PointerField
- [x] Global default map location
- [ ] Streamfield map widget


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Wagtail-Geo-Widget is released under the [MIT License](http://www.opensource.org/licenses/MIT).

