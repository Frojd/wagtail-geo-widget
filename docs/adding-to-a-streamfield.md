## StreamField

To add a map in a StreamField, import and use the GeoBlock.

```python
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtailgeowidget.blocks import GeoBlock

class GeoStreamPage(Page):
    body = StreamField([
        ('map', GeoBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
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

Make sure you define a field representing the address at the same level as your GeoBlock, either in the StreamField or in a StructBlock.

```python
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtailgeowidget.blocks import GeoBlock, GeoAddressBlock


class GeoStreamPage(Page):
    body = StreamField([
        ('map_struct', blocks.StructBlock([
            ('address', GeoAddressBlock(required=True)),
            ('map', GeoBlock(address_field='address')),
        ]))

    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
```

For more examples, look at the [example](https://github.com/Frojd/wagtail-geo-widget/blob/develop/example/geopage/models.py#L64).
