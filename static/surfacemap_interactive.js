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
info.updateSurfaceInfo = function(label, value, source, precipitation, min_air_temp, max_air_temp) {
    this._div.innerHTML = "<div style='text-align: right;'><b>"
        + label + "</b></div><div style='text-align: right;'>" 
        + source + "&nbsp;(" + value +")</div>"
        + "<div style='text-align: right;'>rainfall / year " + precipitation + "&nbsp;cm</div>"
        + "<div style='text-align: right;'>avg. monthly T from " + min_air_temp + "&nbsp;&deg;C to "
        + max_air_temp + "&nbsp;&deg;C</div>";
};
info.addTo(map);
var myMarker = L.marker([50, 8.6], {
    draggable: true,
    zIndexOffset: 1000
});

function requestSurfaceData(e) {
    var xhr = new XMLHttpRequest();
    var latlng = e.latlng.wrap();
    xhr.open('GET', './api/get_surface_data' + '?lat=' + latlng.lat + '&lon=' + latlng.lng);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var surface_info = JSON.parse(xhr.responseText);
            if (e.type == 'click') {
                myMarker.setLatLng(latlng);
                if (!map.hasLayer(myMarker)) {
                    myMarker.addTo(map);
                }
                if (!map.getBounds().contains(myMarker.getLatLng())) {
                    map.panInside(myMarker.getLatLng());
                }
            }
	    info.updateSurfaceInfo(
	        surface_info.surface_cover.label, surface_info.surface_cover.value, surface_info.surface_cover.source,
	        surface_info.air_temp_precipitation.annual_precip_cm,
	        surface_info.air_temp_precipitation.min_air_temp, surface_info.air_temp_precipitation.max_air_temp);
            map.attributionControl.addAttribution(surface_info.surface_cover.attribution);
            map.attributionControl.addAttribution(surface_info.air_temp_precipitation.attribution);
        }
    };
    xhr.send();
}

myMarker.on('move', throttle(requestSurfaceData, 100));
map.on('click', requestSurfaceData);
