import folium
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QLabel, QHBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QFont
import os
import sys
import time

class TravelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерактивная карта путешествий")
        self.setGeometry(100, 100, 800, 600)
        
        self.visited_places = set()
        self.total_places = 5
        
        self.initUI()
        self.generate_map()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        self.map_view = QWebEngineView()
        self.map_view.loadFinished.connect(self.on_map_loaded)
        self.update_map()
        layout.addWidget(self.map_view)

        self.progress_label = QLabel("Прогресс: 0%")
        self.progress_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.progress_label)

        button_layout = QHBoxLayout()
        self.place_buttons = []
        for i in range(1, 6):
            button = QPushButton(f"Посетить место {i}")
            button.clicked.connect(lambda checked, place=i: self.visit_place(place))
            button_layout.addWidget(button)
            self.place_buttons.append(button)
        layout.addLayout(button_layout)

        self.challenge_label = QLabel("Челлендж: Посетите 3 места, чтобы получить награду!")
        self.challenge_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.challenge_label)

        self.reward_label = QLabel("")
        self.reward_label.setFont(QFont("Arial", 12))
        self.reward_label.setStyleSheet("color: green;")
        layout.addWidget(self.reward_label)

    def generate_map(self):
        map_object = folium.Map(location=[55.7558, 37.6173], zoom_start=12)

        locations = [
            (55.7558, 37.6173, "Место 1"),
            (55.5657, 37.6515, "Место 2"),
            (55.4657, 37.5515, "Место 3"),
            (55.6657, 37.7515, "Место 4"),
            (55.8657, 37.9515, "Место 5"),
        ]
        for lat, lon, popup in locations:
            folium.Marker([lat, lon], popup=popup).add_to(map_object)

        map_path = "map.html"
        map_object.save(map_path)

    def update_map(self):
        map_path = os.path.join(os.getcwd(), "map.html")
        if os.path.exists(map_path):
            self.map_view.setUrl(QUrl.fromLocalFile(map_path + "?t=" + str(time.time())))
        else:
            print(f"Ошибка: файл {map_path} не найден!")

    def on_map_loaded(self):
        print("Карта успешно загружена!")

    def visit_place(self, place):
        if place not in self.visited_places:
            self.visited_places.add(place)
            self.update_progress()

    def update_progress(self):
        progress = len(self.visited_places) / self.total_places * 100
        self.progress_label.setText(f"Прогресс: {progress:.0f}%")
        
        if len(self.visited_places) >= 3:
            self.reward_label.setText("Награда получена: Значок исследователя!")
        else:
            self.reward_label.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TravelApp()
    window.show()
    sys.exit(app.exec())
