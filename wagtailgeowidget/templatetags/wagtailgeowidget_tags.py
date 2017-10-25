from django.template import Library
from django.utils.safestring import mark_safe

from wagtailgeowidget.app_settings import (
    GEO_WIDGET_DEFAULT_LOCATION,
    GEO_WIDGET_ZOOM,
    GOOGLE_MAPS_V3_APIKEY,
)

register = Library()


@register.simple_tag
def render_map(map, style):
    return mark_safe(
        '<div class={} id={}></div>'.format(style, map['srid']) +
        """
        <script>
            function initMap() {{
                var point = {{lat: {}, lng: {}}};
                var map = new google.maps.Map(document.getElementById('{}'), {{
                    zoom: {},
                    center: point
                }});
                var marker = new google.maps.Marker({{
                    position: point,
                    map: map
                }});
            }}
        </script>
        """.format(
            map['lat'],
            map['lng'],
            map['srid'],
            GEO_WIDGET_ZOOM
        ) +
        """
            <script async defer src="https://maps.googleapis.com/maps/api/js?key={}&callback=initMap">
            </script>
        """.format(
            GOOGLE_MAPS_V3_APIKEY,
        )
    )
