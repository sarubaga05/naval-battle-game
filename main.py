# Главный файл проекта
from random import randrange


class BoardOutException(Exception):  # Класс исключение: выбор точки за границей поля
    pass


class WrongCellException(Exception):  # Класс исключение: выбор точки, которая уже была выбрана ранее
    pass


class Dot:  # Класс точек на поле
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{self.x, self.y}'