import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

SCREEN_SIZE = [600, 600]


class MapParams(object):
    def __init__(self, lat=0, lon=0, zoom=16):
        self.lat = 61.665279  # Координаты центра карты на старте. Задал координаты университета
        self.lon = 50.813492
        self.zoom = 16  # Масштаб карты на старте. Изменяется от 1 до 19
        self.type = "map"  # Другие значения "sat", "sat,skl"

    # Преобразование координат в параметр ll, требуется без пробелов, через запятую и без скобок
    def ll(self):
        return str(self.lon) + "," + str(self.lat)


def load_map(ll, zoom=16, c="map"):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=ll, z=zoom, type=c)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запись полученного изображения в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('window.ui', self)  # Загружаем дизайн
        self.startButton.clicked.connect(self.run)

    def run(self):
        self.image.setPixmap(QPixmap(load_map(self.coordsEdit.text(), self.scaleEdit.value())))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
