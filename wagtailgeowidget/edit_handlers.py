from wagtail.admin.edit_handlers import FieldPanel

from wagtailgeowidget.app_settings import GEO_WIDGET_ZOOM
from wagtailgeowidget.widgets import GeoField


class GeoPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        self.classname = kwargs.pop("classname", "")
        self.address_field = kwargs.pop("address_field", "")
        self.zoom_field = kwargs.pop("zoom_field", "")
        self.hide_latlng = kwargs.pop("hide_latlng", False)
        self.zoom = kwargs.pop("zoom", GEO_WIDGET_ZOOM)

        super().__init__(*args, **kwargs)

    def widget_overrides(self):
        field = self.model._meta.get_field(self.field_name)
        srid = getattr(field, "srid", 4326)

        return {
            self.field_name: GeoField(
                address_field=self.address_field,
                zoom_field=self.zoom_field,
                hide_latlng=self.hide_latlng,
                zoom=self.zoom,
                srid=srid,
                id_prefix="id_",
                used_in="GeoPanel",
            )
        }

    def clone(self):
        return self.__class__(
            field_name=self.field_name,
            classname=self.classname,
            address_field=self.address_field,
            zoom_field=self.zoom_field,
            hide_latlng=self.hide_latlng,
            zoom=self.zoom,
        )
