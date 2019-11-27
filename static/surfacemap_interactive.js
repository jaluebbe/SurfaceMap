var throttle = function throttle(func, limit) {
  var inThrottle;
  return function () {
    var args = arguments;
    var context = this;

    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(function () {
        return inThrottle = false;
      }, limit);
    }
  };
};

var info = L.control({position: 'bottomright'});
info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.showText('Click on the map to place a marker!<br>You can drag that marker.');
    return this._div;
};
info.showText = function(infoText) {
    this._div.innerHTML = infoText;
};
info.updateSurfaceInfo = function(label, value, source) {
    this._div.innerHTML = "<div style='text-align: right;'><b>"
        + label + "</b></div><div style='text-align: right;'>" 
        + source + '&nbsp;(' + value +')</div>';
};
info.addTo(map);
var myMarker = L.marker([50, 8.6], {
    draggable: true,
    zIndexOffset: 1000
});
myMarker.bindTooltip("", {
    direction: 'top'
});

function requestSurfaceData(e) {
    var xhr = new XMLHttpRequest();
    var latlng = e.latlng.wrap();
    xhr.open('GET', './api/get_surface_data' + '?lat=' + latlng.lat + '&lon=' + latlng.lng);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var surface_info = JSON.parse(xhr.responseText);
            if (e.type == 'click' || e.type == 'locationfound') {
                myMarker.setLatLng(latlng);
                if (!map.hasLayer(myMarker)) {
                    myMarker.addTo(map);
                }
                if (!map.getBounds().contains(myMarker.getLatLng())) {
                    map.panInside(myMarker.getLatLng());
                }
            }
            myMarker._tooltip.setContent("<div style='text-align: center;'><b>"
                + surface_info.label + "</b></div><div style='text-align: center;'>"
                + surface_info.source + '&nbsp;(' + surface_info.value + ')</div>');
	    info.updateSurfaceInfo(surface_info.label, surface_info.value, surface_info.source);
            map.attributionControl.addAttribution(surface_info.attribution);
        }
    };
    xhr.send();
}

myMarker.on('move', throttle(requestSurfaceData, 100));
map.on('click', requestSurfaceData);
map.on('locationfound', requestSurfaceData);
map.locate();
