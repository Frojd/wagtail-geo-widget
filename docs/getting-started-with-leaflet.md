# Getting started with Leaflet

### Requirements

- Python 3.7+
- Wagtail 2.15+ and Django
- Access to a tile provider for Leaflet, this library includes built in support for Open Street Map


### Installation

Install the library with pip:

```
$ pip install wagtailgeowidget
```


### Setup

Add `wagtailgeowidget` to your `INSTALLED_APPS` in Django settings.

```python
INSTALLED_APPS = (
    # ...
    'wagtailgeowidget',
)
```

### Adding to a page

```python
from django.db import models
from wagtail.models import Page
from wagtailgeowidget.edit_handlers import LeafletPanel


class MyPage(Page):
    location = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        LeafletPanel('location'),
    ]
```

### Adding to a stream field

```python
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtailgeowidget.blocks import LeafletBlock

class GeoStreamPage(Page):
    body = StreamField([
        ('map', LeafletBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
```

### Changing tile provider to Mapbox

You can change tile provider by changing the url from where tiles are loaded, this example is for Mapbox but changing to another provider is the same procedure.

- Begin by [obtaining a access token from MapBox](https://docs.mapbox.com/help/getting-started/access-tokens/)

- Include this in your django settings

```python
MAPBOX_ACCESS_TOKEN = "<YOUR MAPBOX ACCESS TOKEN>"
GEO_WIDGET_LEAFLET_TILE_LAYER = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=" + MAPBOX_ACCESS_TOKEN

GEO_WIDGET_LEAFLET_TILE_LAYER_OPTIONS = {
    "attribution": '© <a href="https://www.mapbox.com/feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}
```

### Whats next?

Depending on your use case you can read either of these guides:

- [Adding the widget to a Page](./adding-to-a-page.md)
- [Integrating with GeoDjango](./integrating-with-geodjango.md)
- [Adding to a StreamField](./adding-to-a-streamfield.md)
