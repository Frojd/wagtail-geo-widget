from django.conf import settings

GEO_WIDGET_DEFAULT_LOCATION = getattr(
    settings, "GEO_WIDGET_DEFAULT_LOCATION", {"lat": 59.3293, "lng": 18.0686}
)
GEO_WIDGET_EMPTY_LOCATION = getattr(settings, "GEO_WIDGET_EMPTY_LOCATION", False)
GEO_WIDGET_ZOOM = getattr(settings, "GEO_WIDGET_ZOOM", 7)

GEO_WIDGET_LEAFLET_TILE_LAYER = getattr(
    settings,
    "GEO_WIDGET_LEAFLET_TILE_LAYER",
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
)
GEO_WIDGET_LEAFLET_TILE_LAYER_OPTIONS = getattr(
    settings,
    "GEO_WIDGET_LEAFLET_TILE_LAYER_OPTIONS",
    {
        "attribution": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    },
)

GOOGLE_MAPS_V3_APIKEY = getattr(settings, "GOOGLE_MAPS_V3_APIKEY", None)
GOOGLE_MAPS_V3_APIKEY_CALLBACK = getattr(
    settings, "GOOGLE_MAPS_V3_APIKEY_CALLBACK", None
)
GOOGLE_MAPS_V3_LANGUAGE = getattr(settings, "GOOGLE_MAPS_V3_LANGUAGE", "en")

MAPBOX_ACCESS_TOKEN = getattr(settings, "MAPBOX_ACCESS_TOKEN", None)
MAPBOX_LANGUAGE = getattr(settings, "MAPBOX_LANGUAGE", "en")
