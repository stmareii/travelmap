// Создание карты с начальной точкой в Москве
var map = L.map('map').setView([55.7558, 37.6173], 13); // Координаты Москвы и масштаб

// Добавление базового слоя карты
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Добавление маркеров
var marker1 = L.marker([55.7558, 37.6173]).addTo(map); // Маркер в Москве
marker1.bindPopup("<b>Привет!</b><br>Это Москва.").openPopup();

// Добавление других объектов, например, круг и многоугольник
var circle = L.circle([55.758, 37.617], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 500
}).addTo(map);
circle.bindPopup("Это круг.");

var polygon = L.polygon([
    [55.759, 37.610],
    [55.760, 37.620],
    [55.755, 37.625]
]).addTo(map);
polygon.bindPopup("Это многоугольник.");
