# Getting started

### Requirements

- Python 2.7 / Python 3.5+
- Wagtail 2.3+ and Django
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


### Retriving a Google Maps Api key

- Follow [Googles guide](https://developers.google.com/maps/documentation/javascript/get-api-key) on how to retrive a api key
    - Open the link then click the "Get Started"
- Enable the following services:
    - [Geocoding API](https://developers.google.com/maps/documentation/javascript/geocoding)
	- [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/tutorial)

- When you have the key, add it to your Django settings as `GOOGLE_MAPS_V3_APIKEY`

    ```
    GOOGLE_MAPS_V3_APIKEY = "yourapikey"
    ```


### Whats next?

Depending on your use case you can read either of these guides:

- [Adding the widget to a Page](./adding-to-a-page.md)
- [Integrating with GeoDjango](./integrating-with-geodjango.md)
- [Adding to a StreamField](./adding-to-a-streamfield.md)
