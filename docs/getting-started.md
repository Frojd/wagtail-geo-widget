# Getting started

### Requirements

- Python 3.7+
- Wagtail 2.11+ and Django
- A Google account


### Installation

Install the library with pip:

```
$ pip install wagtailgeowidget
```


### Quick Setup

Add `wagtailgeowidget` to your `INSTALLED_APPS` in Django settings.

```python
INSTALLED_APPS = (
    # ...
    'wagtailgeowidget',
)
```


### Retriving a Google Maps API key

- Follow [Google's guide](https://developers.google.com/maps/documentation/javascript/get-api-key) on how to retrive an API key
    - Open the link then click the `Get Started`
- Enable the following services:
    - [Geocoding API](https://developers.google.com/maps/documentation/geocoding/)
    - [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/)
    - [Places API](https://developers.google.com/places/web-service/)
    - [Maps Static API](https://developers.google.com/maps/documentation/maps-static/)

- When you have the key, add it to your Django settings as `GOOGLE_MAPS_V3_APIKEY`

    ```
    GOOGLE_MAPS_V3_APIKEY = "yourapikey"
    ```


### Whats next?

Depending on your use case you can read either of these guides:

- [Adding the widget to a Page](./adding-to-a-page.md)
- [Integrating with GeoDjango](./integrating-with-geodjango.md)
- [Adding to a StreamField](./adding-to-a-streamfield.md)
