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


class Ship:  # Класс корабля
    def __init__(self, lenght, start_dot, direction):
        self.lenght = lenght
        self.start_dot = start_dot
        self.direction = direction
        self.hp = lenght

    @property
    def dots(self):  # Список точек корабля
        ship_dots = []
        for i in range(self.lenght):
            x1 = self.start_dot.x
            y1 = self.start_dot.y

            if self.direction == 0:
                x1 += i
            elif self.direction == 1:
                y1 += i

            ship_dots.append(Dot(x1, y1))
        return ship_dots
