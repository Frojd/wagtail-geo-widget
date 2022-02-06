## FAQ

### Is it possible to hide the lat/lng field?

Yes, by passing `hide_latlng=True` to the GeoPanel.

```python
GoogleMapsPanel('location', address_field='address', hide_latlng=True)
```

For streamfields use the following:

```python
GoogleMapsBlock(address_field='address', hide_latlng=True)
```


### How can I make the Google Maps API key editable in the admin?

By using `GOOGLE_MAPS_V3_APIKEY_CALLBACK` you can implement a custom behaviour for retriving api key, this will ignore `GOOGLE_MAPS_V3_APIKEY`. Implementation example:


```python
# settings.py
GOOGLE_MAPS_V3_APIKEY_CALLBACK = "home.helpers.get_apikey"
```

```python
# home/helpers.py 
def get_apikey():
    from home.models import GeoWidgetSettings

    settings = GeoWidgetSettings.objects.first()
    return settings.google_maps_apikey
```

```python
# home/models.py
from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel

@register_setting
class GeoWidgetSettings(BaseSetting):
    google_maps_apikey = models.CharField(
        help_text="Google maps api key", max_length=255
    )

    panels = [
        FieldPanel("google_maps_apikey"),
    ]
```


### Is it possible to hide the zoom field?

Yes, by adding the css class `geo-field-zoom--hide` you can hide the field in the admin.

- Field panel:
    ```python
    FieldPanel("zoom", classname="geo-field-zoom--hide")
    ```

- In streamfield:
    ```python
    ('zoom', GeoZoomBlock(required=False, form_classname="geo-field-zoom--hide")),
    ```
