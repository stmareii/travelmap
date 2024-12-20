from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QLabel, QHBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QFont
import os
import sys
import folium

# Класс для основного приложения
class TravelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерактивная карта путешествий")
        self.setGeometry(100, 100, 800, 600)
        
        # Инициализация посещённых мест и прогресса
        self.visited_places = set()
        self.total_places = 5  # Всего 5 точек на карте
        
        # Настройка интерфейса
        self.initUI()

        # Генерация карты
        self.generate_map()

    def initUI(self):
        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Отображение карты из файла map.html
        self.map_view = QWebEngineView()
        self.map_view.loadFinished.connect(self.on_map_loaded)  # Обработчик завершения загрузки
        self.update_map()
        layout.addWidget(self.map_view)

        # Прогресс
        self.progress_label = QLabel("Прогресс: 0%")
        self.progress_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.progress_label)

        # Кнопки для симуляции посещения мест
        button_layout = QHBoxLayout()
        self.place_buttons = []
        for i in range(1, 6):  # Создаём 5 мест
            button = QPushButton(f"Посетить место {i}")
            button.clicked.connect(lambda checked, place=i: self.visit_place(place))
            button_layout.addWidget(button)
            self.place_buttons.append(button)
        layout.addLayout(button_layout)

        # Метка челленджа
        self.challenge_label = QLabel("Челлендж: Посетите 3 места, чтобы получить награду!")
        self.challenge_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.challenge_label)

        # Метка награды
        self.reward_label = QLabel("")
        self.reward_label.setFont(QFont("Arial", 12))
        self.reward_label.setStyleSheet("color: green;")
        layout.addWidget(self.reward_label)

    def generate_map(self):
    # Генерация карты с помощью folium (с изменением начальной точки на Москву)
        map_object = folium.Map(location=[55.7558, 37.6173], zoom_start=12)  # Центр в Москве

        # Добавление 5 маркеров на карту
        locations = [
            (55.7558, 37.6173, "Место 1"),  # Москва
            (55.5657, 37.6515, "Место 2"),
            (55.4657, 37.5515, "Место 3"),
            (55.6657, 37.7515, "Место 4"),
            (55.8657, 37.9515, "Место 5"),
        ]
        for lat, lon, popup in locations:
            folium.Marker([lat, lon], popup=popup).add_to(map_object)

        # Добавление CDN для библиотеки Leaflet, если необходимо
        map_html = map_object.get_root().render()
        map_html = map_html.replace('<head>', '''<head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>''')

        # Сохранение карты
        map_path = "map.html"
        with open(map_path, 'w', encoding='utf-8') as f:
            f.write(map_html)

        # Проверка, что карта создана
        if os.path.exists(map_path):
            print(f"Карта успешно создана: {os.path.abspath(map_path)}")
        else:
            print("Ошибка: карта не создана!")

    def update_map(self):
        # Обновление карты
        map_path = os.path.join(os.getcwd(), "map.html")
        if os.path.exists(map_path):
            self.map_view.setUrl(QUrl.fromLocalFile(map_path))  # Загрузка карты
        else:
            print(f"Ошибка: файл {map_path} не найден!")

    def on_map_loaded(self):
        # Обработчик загрузки карты, можно обновить интерфейс или сделать другие действия
        print("Карта успешно загружена!")

    def visit_place(self, place):
        # Отметить место как посещённое, если оно ещё не посещено
        if place not in self.visited_places:
            self.visited_places.add(place)
            self.update_progress()

    def update_progress(self):
        # Обновление прогресса
        progress = len(self.visited_places) / self.total_places * 100
        self.progress_label.setText(f"Прогресс: {progress:.0f}%")
        
        # Проверка выполнения челленджа
        if len(self.visited_places) >= 3:
            self.reward_label.setText("Награда получена: Значок исследователя!")
        else:
            self.reward_label.setText("")

if __name__ == "__main__":
    # Запуск графического интерфейса
    app = QApplication(sys.argv)
    window = TravelApp()
    window.show()
    sys.exit(app.exec())
