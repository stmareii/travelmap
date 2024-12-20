// leafnet.js
document.addEventListener("DOMContentLoaded", function () {
    // Initialize map
    const map = L.map("map").setView([55.7558, 37.6173], 12);

    // Add OpenStreetMap tiles
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    // Define locations with coordinates and descriptions
    const locations = [
        { lat: 55.7558, lon: 37.6173, name: "Место 1" },
        { lat: 55.5657, lon: 37.6515, name: "Место 2" },
        { lat: 55.4657, lon: 37.5515, name: "Место 3" },
        { lat: 55.6657, lon: 37.7515, name: "Место 4" },
        { lat: 55.8657, lon: 37.9515, name: "Место 5" },
    ];

    // Add markers to the map
    locations.forEach(({ lat, lon, name }) => {
        const marker = L.marker([lat, lon]).addTo(map);
        marker.bindPopup(name);

        marker.on("click", function () {
            handlePlaceVisit(name);
        });
    });

    // Handle place visits and update progress
    const visitedPlaces = new Set();
    const totalPlaces = locations.length;
    const progressLabel = document.getElementById("progress-label");
    const rewardLabel = document.getElementById("reward-label");

    function handlePlaceVisit(placeName) {
        if (!visitedPlaces.has(placeName)) {
            visitedPlaces.add(placeName);
            updateProgress();
        }
    }

    function updateProgress() {
        const progress = (visitedPlaces.size / totalPlaces) * 100;
        progressLabel.textContent = `Прогресс: ${progress.toFixed(0)}%`;

        if (visitedPlaces.size >= 3) {
            rewardLabel.textContent = "Награда получена: Значок исследователя!";
        } else {
            rewardLabel.textContent = "";
        }
    }
});
