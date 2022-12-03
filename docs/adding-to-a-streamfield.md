## StreamField

This documents explains how to add a Google Maps map in a StreamField.

If you instead want to use Leaflet, just change `GoogleMapsBlock` to `LeafletBlock`

```python
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtailgeowidget.blocks import GoogleMapsBlock

class GeoStreamPage(Page):
    body = StreamField([
        ('map', GoogleMapsBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
```

The data is stored as a json struct and you can access it by using value.lat / value.lng

```html
<article>
    {% for map_block in page.stream_field %}
        <hr />
        {{ map_block.value }}
        <p>Latitude: {{ map_block.value.lat}}</p>
        <p>Longitude: {{ map_block.value.lng }}</p>
    {% endfor %}
</article>
```

### With an address field

The address block supports several different geocoding services, but in this example below we use the Google Maps Geocoding service. You change the geocoder service by changing the geocoder param.

Make sure you define a field representing the address at the same level as your GoogleMapsBlock, either in the StreamField or in a StructBlock.

```python
from wagtail.admin.panels import FieldPanel
from wagtailgeowidget import geocoders
from wagtailgeowidget.blocks import GoogleMapsBlock, GeoAddressBlock


class GeoStreamPage(Page):
    body = StreamField([
        ('map_struct', blocks.StructBlock([
            ('address', GeoAddressBlock(required=True, geocoder=geocoders.GOOGLE_MAPS)),
            ('map', GoogleMapsBlock(address_field='address')),
        ]))
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
```


### With an zoom field

Define a field representing the zoom at the same level as your GoogleMapsBlock, either in the StreamField or in a StructBlock.

```python
from wagtail.admin.panels import FieldPanel
from wagtailgeowidget.blocks import GoogleMapsBlock, GeoZoomBlock


class GeoStreamPage(Page):
    body = StreamField([
        ('map_struct', blocks.StructBlock([
            ('zoom', GeoZoomBlock(required=False)),
            ('map', GoogleMapsBlock(zoom_field='zoom')),
        ]))
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
```


### More examples

For more examples, look at the [example](https://github.com/Frojd/wagtail-geo-widget/blob/develop/tests/geopage/models.py#L149).
