var map = L.map('map').setView([50.0, 8.0], 5);
map.attributionControl.addAttribution(
    '<a href="https://github.com/jaluebbe/SurfaceMap">Source on GitHub</a>');
// add link to privacy statement
map.attributionControl.addAttribution(
    '<a href="static/datenschutz.html" target="_blank">Datenschutzerkl&auml;rung</a>');
var wmsLayer = L.tileLayer.wms('https://sgx.geodatenzentrum.de/wms_topplus_open', {
    layers: 'web',
    format: 'image/png',
    transparent: true,
    minZoom: 1,
    attribution: '&copy <a href="https://www.bkg.bund.de">BKG</a> 2019, ' +
        '<a href= "http://sg.geodatenzentrum.de/web_public/Datenquellen_TopPlus_Open.pdf" >data sources</a> '
}).addTo(map);
L.control.scale({
    'imperial': false
}).addTo(map);
var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});
var otmLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    maxZoom: 15,
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> ' +
        'contributors, SRTM | Map style: &copy; ' +
        '<a href="https://opentopomap.org">OpenTopoMap</a> ' +
        '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});
esriImagery = L.layerGroup([
    L.esri.basemapLayer('Imagery'),
    L.esri.basemapLayer('ImageryLabels')
]);
baseLayers = {
    "TopPlusOpen": wmsLayer,
    "OpenTopoMap": otmLayer,
    "OpenStreetMap": osmLayer,
    "Esri Imagery": esriImagery
};
if (typeof mapboxAccessToken !== 'undefined') {
    var mapbox_streets = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=' +
        mapboxAccessToken, {
            maxZoom: 19,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
                '<a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets'
        });
    var mapbox_streets_satellite = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=' +
        mapboxAccessToken, {
            maxZoom: 19,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; ' +
                '<a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets-satellite'
        });
    Object.assign(baseLayers, {
        "Mapbox Streets": mapbox_streets,
        "MapBox Satellite Streets": mapbox_streets_satellite
    });
}
var other_layers = {};
var layerControl = L.control.layers(baseLayers, other_layers, {
    collapsed: L.Browser.mobile, // hide on mobile devices
    position: 'topright'
}).addTo(map);
