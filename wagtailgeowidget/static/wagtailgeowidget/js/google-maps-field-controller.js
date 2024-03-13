// wagtailgeowidget/static/wagtailgeowidget/js/google-maps-field-controller.js

class GoogleMapsFieldController extends window.StimulusModule.Controller {
    static values = { options: Object };

    connect() {
        let id = this.element.id;
        let namespace = "id_";
        let options = this.optionsValue;
        let addressSelector = options.addressField;
        let zoomSelector = options.zoomField;

        if (id.indexOf("-") !== -1) {
            namespace = id.split("-")
                .slice(0, -1)
                .join("-");
            namespace = namespace + "-";
        }

        if (addressSelector) {
            addressSelector = "#" + namespace + addressSelector;
        }

        if (zoomSelector) {
            zoomSelector = "#" + namespace + zoomSelector;
        }

        options = Object.assign({}, options, {
            "id": id,
            "addressSelector": addressSelector,
            "zoomSelector": zoomSelector,
        });

        new GoogleMapsField(options);
    }
}

window.wagtail.app.register('google-maps-field', GoogleMapsFieldController);
