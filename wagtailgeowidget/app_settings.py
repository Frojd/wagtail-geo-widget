from django.conf import settings

GEO_WIDGET_DEFAULT_LOCATION = getattr(
    settings, "GEO_WIDGET_DEFAULT_LOCATION", {"lat": 59.3293, "lng": 18.0686}
)
GEO_WIDGET_EMPTY_LOCATION = getattr(settings, "GEO_WIDGET_EMPTY_LOCATION", False)
GEO_WIDGET_ZOOM = getattr(settings, "GEO_WIDGET_ZOOM", 7)
GOOGLE_MAPS_V3_APIKEY = getattr(settings, "GOOGLE_MAPS_V3_APIKEY", None)
GOOGLE_MAPS_V3_APIKEY_CALLBACK = getattr(
    settings, "GOOGLE_MAPS_V3_APIKEY_CALLBACK", None
)
GOOGLE_MAPS_V3_LANGUAGE = getattr(settings, "GOOGLE_MAPS_V3_LANGUAGE", "en")
