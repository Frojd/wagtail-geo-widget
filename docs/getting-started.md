# Getting started

Wagtail-Geo-Widget is built in Python as a library to Wagtail, so make sure you Wagtail based website up and running.


## Requirements

- Python 2.7 / Python 3.5+
- Wagtail 2.3+ and Django
- A Google account


## Installation

Install the library with pip:

```
$ pip install wagtailgeowidget
```


## Quick Setup

Make sure `wagtailgeowidget` is added to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = (
    # ...
    'wagtailgeowidget',
)
```


## Retriving a Google Maps Api key

- Follow [Googles guide](https://developers.google.com/maps/documentation/javascript/get-api-key) on how to retrive a api key
    - Open the link then click the "Get Started"
- Enable the following services:
    - [Geocoding API](https://developers.google.com/maps/documentation/javascript/geocoding)
	- [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/tutorial)

- When you have the key, add it to your Django settings as `GOOGLE_MAPS_V3_APIKEY`

    ```
    GOOGLE_MAPS_V3_APIKEY = "yourapikey"
    ```
