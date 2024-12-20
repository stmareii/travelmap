import folium
import os
import sys
import time
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QLabel, QHBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QFont, QIcon
from functools import partial
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

class TravelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерактивная карта путешествий")
        self.setGeometry(100, 100, 800, 600)

        self.visited_places = set()
        self.total_places = 5
        self.dark_mode = False

        self.initUI()
        self.generate_map()
        self.start_server()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Виджет для отображения карты
        self.map_view = QWebEngineView()
        self.map_view.loadFinished.connect(self.on_map_loaded)
        self.update_map()
        layout.addWidget(self.map_view)

        # Метка прогресса
        self.progress_label = QLabel("Прогресс: 0%")
        self.progress_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.progress_label)

        # Кнопки для посещения мест
        button_layout = QHBoxLayout()
        self.place_buttons = []
        for i in range(1, 6):
            button = QPushButton(f"Посетить место {i}")
            button.clicked.connect(partial(self.visit_place, place=i))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #87CEFA;
                    border-radius: 10px;
                    padding: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #4682B4;
                    color: white;
                }
            """)
            button_layout.addWidget(button)
            self.place_buttons.append(button)
        layout.addLayout(button_layout)

        # Текст челленджа
        self.challenge_label = QLabel("Челлендж: Посетите 3 места, чтобы получить награду!")
        self.challenge_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.challenge_label)

        # Метка награды
        self.reward_label = QLabel("")
        self.reward_label.setFont(QFont("Arial", 12))
        self.reward_label.setStyleSheet("color: green;")
        layout.addWidget(self.reward_label)

        # Кнопка переключения темы
        self.theme_button = QPushButton("Переключить тему")
        self.theme_button.setStyleSheet("""
            QPushButton {
                background-color: #d3d3d3;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #a9a9a9;
                color: white;
            }
        """)
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)

        # Установка начальной темы
        self.set_theme()

    def generate_map(self):
        # Генерация карты с местами
        map_object = folium.Map(location=[55.7558, 37.6173], zoom_start=12)

        self.locations = [
            (55.75202, 37.61749, "Московский Кремль"),
            (55.75098, 37.61698, "Успенский собор"),
            (55.75076, 37.61849, "Царь-колокол"),
            (55.74968, 37.6136, "Оружейная палата и Алмазный фонд"),
            (55.760178, 37.618575, "Большой театр"),
        ]

        # Добавление маркеров на карту
        for lat, lon, popup in self.locations:
            folium.Marker([lat, lon], popup=popup).add_to(map_object)

        # Сохранение карты как HTML файл
        self.map_filename = "map.html"
        map_path = os.path.join(os.getcwd(), self.map_filename)
        map_object.save(map_path)
        print(f"Карта сохранена в: {map_path}")

    def update_map(self):
        # Вместо локального пути используем URL локального сервера
        map_url = "http://localhost:8000/map.html"
        self.map_view.setUrl(QUrl(map_url))

    def on_map_loaded(self):
        print("Карта успешно загружена!")

    def visit_place(self, place):
        if place not in self.visited_places:
            self.visited_places.add(place)
            self.update_progress()
            self.update_map_with_progress()

    def update_progress(self):
        # Обновление прогресса
        progress = len(self.visited_places) / self.total_places * 100
        self.progress_label.setText(f"Прогресс: {progress:.0f}%")

        # Проверка на получение награды
        if len(self.visited_places) >= 3:
            self.reward_label.setText("Награда получена: Значок исследователя!")
        else:
            self.reward_label.setText("")

    def update_map_with_progress(self):
        # Обновление карты с учётом посещённых мест
        map_object = folium.Map(location=[55.7558, 37.6173], zoom_start=12)

        for i, (lat, lon, popup) in enumerate(self.locations, start=1):
            color = "green" if i in self.visited_places else "red"
            folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color=color)).add_to(map_object)

        # Сохранение обновленной карты
        map_path = os.path.join(os.getcwd(), self.map_filename)
        map_object.save(map_path)
        self.update_map()

    def toggle_theme(self):
        # Переключение темы
        self.dark_mode = not self.dark_mode
        self.set_theme()

    def set_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2b2b2b;
                    color: white;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #444;
                    color: white;
                    border-radius: 10px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                    color: black;
                }
                QLabel {
                    color: black;
                }
                QPushButton {
                    background-color: #d3d3d3;
                    color: black;
                    border-radius: 10px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #a9a9a9;
                }
            """)

    def start_server(self):
        # Функция для запуска локального сервера
        def run_server():
            os.chdir(os.getcwd())  # Убедитесь, что сервер обслуживает текущую директорию
            server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
            print("Сервер запущен на http://localhost:8000")
            server.serve_forever()

        # Запуск сервера в отдельном потоке
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TravelApp()
    window.show()
    sys.exit(app.exec())
