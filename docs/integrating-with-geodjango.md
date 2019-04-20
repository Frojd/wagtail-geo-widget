# Integrating with GeoDjango

First make sure you have [GeoDjango](https://docs.djangoproject.com/en/1.10/ref/contrib/gis/) correctly setup and a PointField field defined in your model, then add a GeoPanel among your content_panels.

```python
from django.contrib.gis.db import models
from wagtailgeowidget.edit_handlers import GeoPanel


class MyPage(Page):
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        GeoPanel('location'),
    ]
```


### With an address field

The panel accepts an `address_field` if you want to use the map in coordination with a geo-lookup (like the screenshot on top).

```python
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtailgeowidget.edit_handlers import GeoPanel


class MyPageWithAddressField(Page):
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('address'),
            GeoPanel('location', address_field='address'),
        ], _('Geo details')),
    ]
```

For more examples, look at the [example](https://github.com/Frojd/wagtail-geo-widget/blob/develop/example/geopage/models.py).
