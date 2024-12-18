from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
import sys

class TravelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерактивная карта путешествий")
        self.setGeometry(100, 100, 800, 600)
        
        # Инициализация посещённых мест и прогресса
        self.visited_places = set()
        self.total_places = 10  # Общее количество мест (пример)
        
        # Настройка интерфейса
        self.initUI()

    def initUI(self):
        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout =QVBoxLayout()
        main_widget.setLayout(layout)

        # Отображение карты (заглушка для простоты)
        self.map_label = QLabel()
        self.map_label.setPixmap(QPixmap(600, 400))
        self.map_label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        self.map_label.setAlignment(Qt.AlignCenter)
        self.map_label.setText("Здесь будет карта")
        layout.addWidget(self.map_label)

        # Прогресс
        self.progress_label = QLabel("Прогресс: 0%")
        self.progress_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.progress_label)

        # Кнопки для симуляции посещения мест
        button_layout = QHBoxLayout()
        self.place_buttons = []
        for i in range(1, 6):  # Создаём 5 примерных мест
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

    def visit_place(self, place):
        # Отметить место как посещённое
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
    app = QApplication(sys.argv)
    window = TravelApp()
    window.show()
    sys.exit(app.exec_())
