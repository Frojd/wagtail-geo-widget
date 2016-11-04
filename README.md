# Wagtail-Geo-Widget




## Requirements

- Python 2.7 / Python 3.4 / PyPy
- Django 1.8+


## Installation

Install the library with pip:

```
$ pip install wagtail-geo-widget
```


## Quick Setup

Make sure wagtail_geo_widget is added to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = (
    # ...
    'wagtail_geo_widget',
)

```


This should be enough to get started.


## Usage


```python
from wagtailgeowidget.edit_handlers import GeoPanel

class MyPage(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoPanel('location', address_field='address'),
    ]
```


## Settings

- `GOOGLE_MAPS_V3_APIKEY`: Api key for google maps


## Tests

This library include tests, just run `python runtests.py`.


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Wagtail-Geo-Widget is released under the [MIT License](http://www.opensource.org/licenses/MIT).

