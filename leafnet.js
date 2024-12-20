// Инициализация карты и установка начальной точки и масштаба
var map = L.map('map').setView([51.505, -0.09], 13);

// Добавление базового слоя карты (например, OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Добавление маркера
var marker = L.marker([51.505, -0.09]).addTo(map);
marker.bindPopup("<b>Привет!</b><br>Это Лондон.").openPopup();

// Добавление круга
var circle = L.circle([51.508, -0.11], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 500
}).addTo(map);
circle.bindPopup("Это круг.");

// Добавление многоугольника
var polygon = L.polygon([
    [51.509, -0.08],
    [51.503, -0.06],
    [51.51, -0.047]
]).addTo(map);
polygon.bindPopup("Это многоугольник.");

// Добавление всплывающей подсказки при клике на карту
map.on('click', function(e) {
    L.popup()
        .setLatLng(e.latlng)
        .setContent("Вы кликнули в точке " + e.latlng.toString())
        .openOn(map);
});
