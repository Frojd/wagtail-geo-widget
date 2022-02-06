# Settings

- `GOOGLE_MAPS_V3_APIKEY`: API key for Google Maps (required).
- `GOOGLE_MAPS_V3_LANGUAGE`: The language you want to set for the map interface (default is `en`)
- `GEO_WIDGET_DEFAULT_LOCATION`: Default map location when no coordinates are set, accepts a dict with lat and lng keys (default is `{'lat': 59.3293, 'lng': 18.0686}` that is Stockholm/Sweden).
- `GEO_WIDGET_ZOOM`: Default zoom level for map (7 is default).
- `GEO_WIDGET_EMPTY_LOCATION`: Defaults to False. If set to True it allows location fields to be optional. When interacting with a location/address field the map will be initialized.
- `GOOGLE_MAPS_V3_APIKEY_CALLBACK`: Dotted path to a function used for retrieving Google Maps API Key dynamically (ex `mymodule.helpers.get_apikey`). Defaults to None.

    ```python
    # example function
    def get_apikey():
        from home.models import GeoWidgetSettings

        settings = GeoWidgetSettings.objects.first()
        return settings.google_maps_apikey
    ```

- `GEO_WIDGET_LEAFLET_TILE_LAYER`: Which title provider to use in Leaflet. By default it is OSM. (`https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`).
- `GEO_WIDGET_LEAFLET_TILE_LAYER_OPTIONS`: The tile layer options for leaflet, it supports [the following arguments](https://leafletjs.com/reference.html). Default is `{"attribution": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}`
