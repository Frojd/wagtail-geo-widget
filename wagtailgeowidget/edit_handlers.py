from wagtail.admin.edit_handlers import FieldPanel

from wagtailgeowidget.widgets import (
    GeoField,
)


class GeoPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        self.classname = kwargs.pop('classname', "")
        self.address_field = widget = kwargs.pop('address_field', "")
        self.zoom = kwargs.pop('zoom', 7)

        super().__init__(*args, **kwargs)

    def widget_overrides(self):
        field = self.model._meta.get_field(self.field_name)
        srid = getattr(field, 'srid', 4326)

        return {
            self.field_name: GeoField(
                address_field=self.address_field,
                zoom=self.zoom,
                srid=srid,
                id_prefix='id_',
            )
        }

    def clone(self):
        return self.__class__(
            field_name=self.field_name,
            classname=self.classname,
            address_field=self.address_field,
            zoom=self.zoom,
        )
