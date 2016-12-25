from wagtail.wagtailadmin.edit_handlers import BaseFieldPanel

from wagtailgeowidget.widgets import GeoField


class GeoPanel(BaseFieldPanel):
    def __init__(self, field_name, classname="", address_field="", zoom=7):
        self.field_name = field_name
        self.classname = classname
        self.address_field = address_field
        self.zoom = zoom

    def bind_to_model(self, model):
        field = model._meta.get_field(self.field_name)

        widget = type(str('_GeoField'), (GeoField,), {
            'address_field': self.address_field,
            'zoom': self.zoom,
            'srid': field.srid,
        })

        base = {
            'model': model,
            'field_name': self.field_name,
            'classname': self.classname,
            'widget': widget,
        }

        out = type(str('_GeoPanel'), (BaseFieldPanel,), base)
        return out
