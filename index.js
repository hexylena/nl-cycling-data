const map = L.map('map').setView([52.05, 4.3], 12);
const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const rdLayer = L.geoJSON(rd_boxes).addTo(map);

function onEachFeature(feature, layer) {
	let popupContent = `<p>I started out as a GeoJSON ${feature.geometry.type}, but now I'm a Leaflet vector!</p>`;

	if (feature.properties) {
		popupContent += JSON.stringify(feature.properties);
	}

	layer.bindPopup(popupContent);
}

const coorsLayer = L.geoJSON(gj, {
	pointToLayer(feature, latlng) {
		return L.circleMarker(latlng, {'color': 'blue', radius: 5});
	},
	onEachFeature
}).addTo(map);
