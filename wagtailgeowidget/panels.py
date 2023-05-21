from wagtail.admin.panels import FieldPanel

from wagtailgeowidget import geocoders
from wagtailgeowidget.app_settings import GEO_WIDGET_ZOOM
from wagtailgeowidget.widgets import GeocoderField, GoogleMapsField, LeafletField


class GoogleMapsPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        self.classname = kwargs.pop("classname", "")
        self.address_field = kwargs.pop("address_field", "")
        self.zoom_field = kwargs.pop("zoom_field", "")
        self.hide_latlng = kwargs.pop("hide_latlng", False)
        self.zoom = kwargs.pop("zoom", GEO_WIDGET_ZOOM)

        super().__init__(*args, **kwargs)

    def get_form_options(self):
        opts = super().get_form_options()
        opts["widgets"] = self.widget_overrides()
        return opts

    def widget_overrides(self):
        field = self.model._meta.get_field(self.field_name)
        srid = getattr(field, "srid", 4326)

        return {
            self.field_name: GoogleMapsField(
                address_field=self.address_field,
                zoom_field=self.zoom_field,
                hide_latlng=self.hide_latlng,
                zoom=self.zoom,
                srid=srid,
                id_prefix="id_",
            )
        }

    def clone(self):
        return self.__class__(
            address_field=self.address_field,
            zoom_field=self.zoom_field,
            hide_latlng=self.hide_latlng,
            zoom=self.zoom,
            **self.clone_kwargs(),
        )


class GeoPanel(GoogleMapsPanel):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            "GeoPanel will be deprecated in version 7, use GoogleMapsPanel instead",
            PendingDeprecationWarning,
        )

        super().__init__(*args, **kwargs)


class GeoAddressPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        self.geocoder = kwargs.pop("geocoder", geocoders.NOMINATIM)

        super().__init__(*args, **kwargs)

    def get_form_options(self):
        opts = super().get_form_options()
        opts["widgets"] = self.widget_overrides()
        return opts

    def widget_overrides(self):
        return {
            self.field_name: GeocoderField(
                geocoder=self.geocoder,
            )
        }

    def clone(self):
        return self.__class__(
            geocoder=self.geocoder,
            **self.clone_kwargs(),
        )


class LeafletPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        self.classname = kwargs.pop("classname", "")
        self.address_field = kwargs.pop("address_field", "")
        self.zoom_field = kwargs.pop("zoom_field", "")
        self.hide_latlng = kwargs.pop("hide_latlng", False)
        self.zoom = kwargs.pop("zoom", GEO_WIDGET_ZOOM)

        super().__init__(*args, **kwargs)

    def get_form_options(self):
        opts = super().get_form_options()
        opts["widgets"] = self.widget_overrides()
        return opts

    def widget_overrides(self):
        field = self.model._meta.get_field(self.field_name)
        srid = getattr(field, "srid", 4326)

        return {
            self.field_name: LeafletField(
                address_field=self.address_field,
                zoom_field=self.zoom_field,
                hide_latlng=self.hide_latlng,
                zoom=self.zoom,
                srid=srid,
                id_prefix="id_",
            )
        }

    def clone(self):
        return self.__class__(
            address_field=self.address_field,
            zoom_field=self.zoom_field,
            hide_latlng=self.hide_latlng,
            zoom=self.zoom,
            **self.clone_kwargs(),
        )
