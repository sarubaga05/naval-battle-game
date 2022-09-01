# Главный файл проекта
from random import randrange
import time


class BoardOutException(Exception):  # Класс исключение: выбор точки за границей поля
    pass


class WrongCellException(Exception):  # Класс исключение: выбор точки, которая уже была выбрана ранее
    pass


class WrongShipException(Exception):  # Класс исключение: вызываем при ошибке взаимодействия с кораблем
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


class Board:
    def __init__(self, hid=False):
        self.cell_list = [['O', 'O', 'O', 'O', 'O', 'O'],
                          ['O', 'O', 'O', 'O', 'O', 'O'],
                          ['O', 'O', 'O', 'O', 'O', 'O'],
                          ['O', 'O', 'O', 'O', 'O', 'O'],
                          ['O', 'O', 'O', 'O', 'O', 'O'],
                          ['O', 'O', 'O', 'O', 'O', 'O']]
        self.ship_list = []
        self.hid = hid
        self.count_ship = 7
        self.used_dots = []

    def add_ship(self, ship):  # Добавление корабля
        for dot in ship.dots:
            if self.out(dot) or dot in self.used_dots:
                raise WrongShipException()
        for dot in ship.dots:
            self.cell_list[dot.x][dot.y] = "■"
            self.used_dots.append(dot)

        self.ship_list.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):  # Обводка корабля
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)
                ]
        for dot in ship.dots:
            for x1, y1 in near:
                new_dot = Dot(dot.x + x1, dot.y + y1)
                if not (self.out(new_dot)) and not (new_dot in self.used_dots):
                    if verb:
                        self.cell_list[new_dot.x][new_dot.y] = "T"
                    self.used_dots.append(new_dot)

    def show_board(self):  # Вывод игрового поля
        brd = ""
        brd += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.cell_list):
            brd += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            brd = brd.replace("■", "O")
        return brd

    def out(self, dot):  # Проверка: выходит ли выбранная ячейка за границы игрового поля
        if not (0 <= dot.x < 6) or not (0 <= dot.y < 6):
            return True
        else:
            return False

    def shot(self, dot):  # Выстрел по игровому полю
        if self.out(dot):
            raise BoardOutException()
        if dot in self.used_dots:
            raise WrongCellException()

        self.used_dots.append(dot)

        for ship in self.ship_list:
            if dot in ship.dots:
                ship.hp -= 1
                self.cell_list[dot.x][dot.y] = "X"
                if ship.hp == 0:
                    self.count_ship -= 1
                    self.contour(ship, verb=True)
                    print("Подбил!")
                    return True
                else:
                    print("Ранил!")
                    return True

        self.cell_list[dot.x][dot.y] = "T"
        print("Мимо!")
        return False

    def clean_used_dots(self):  # Очистка списка использованных точек после формирования доскиы
        self.used_dots = []


class Player:  # Общие методы для игрока и AI
    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                selected_dot = self.ask()
                shot1 = self.enemy_board.shot(selected_dot)
                return shot1
            except BoardOutException:
                print('Такой ячейки на поле нет!')
            except WrongCellException:
                print('Данную ячейку нельзя использовать!')


class AI(Player):  # Случайный выбор точки для выстрела
    def ask(self):
        new_x = randrange(6)
        new_y = randrange(6)
        print(f'Компьютер выстрелил в точку {new_x + 1} {new_y + 1}')
        return Dot(new_x, new_y)


class User(Player):
    def ask(self):
        while True:
            new_x = input("Введите координату x (номер строки): ")
            new_y = input("Введите координату y (номер столбца): ")

            if not(new_x.isdigit()) or not(new_y.isdigit()):
                print('Были введены не числа.')
                continue

            if len(new_x) > 1 or len(new_y) > 1:
                print('Числа введены некорректно.')
                continue

            new_x = int(new_x)
            new_y = int(new_y)
            return Dot(new_x - 1, new_y - 1)


class Game:  # Класс игрового процесса
    def __init__(self):
        user_board = self.random_board()
        ai_board = self.random_board()
        self.user = User(user_board, ai_board)
        self.ai = AI(ai_board, user_board)
        ai_board.hid = True

    def random_board(self):  # Генерация доски
        board = None
        while board is None:
            board = self.spread_ship()
        return board

    def spread_ship(self):  # Расстановка кораблей на поле
        board = Board()
        num_of_attempts = 0
        ship_lenght = [3, 2, 2, 1, 1, 1, 1]
        for lenght in ship_lenght:
            while True:
                num_of_attempts += 1
                if num_of_attempts > 3000:
                    return None
                ship = Ship(lenght, Dot(randrange(6), randrange(6)), randrange(2))
                try:
                    board.add_ship(ship)
                    break
                except WrongShipException:
                    pass
        board.clean_used_dots()
        return board

    def greet(self):  # Приветствие при старте игры
        print('Приветствую вас в игре Морской бой!')
        time.sleep(2)
        print('...')
        time.sleep(2)
        print('Правила очень просты - уничтожить все корабли противника')
        time.sleep(2)
        print('Игра проходит против компьютера')
        time.sleep(2)
        print('Ходы идут по очереди. Если кто-то попал в корабль, то делает ход повторно')
        time.sleep(2)
        print('При ходе нужны ввести координаты - число от 1 до 6')
        time.sleep(2)
        print('Удачной игры!')
        time.sleep(2)

    def loop(self):  # Игровой цикл
        flag = 0
        while True:
            print('...')
            print('Ваша доска:')
            print(self.user.my_board.show_board())
            time.sleep(1)
            print('...')
            print('Доска компьютера:')
            print(self.ai.my_board.show_board())
            time.sleep(1)
            if flag % 2 == 0:
                print('...')
                print('Ваш ход')
                new_move = self.user.move()
                time.sleep(2)
            else:
                print('...')
                print('Ход компьютера')
                new_move = self.ai.move()
                time.sleep(2)
            if new_move:
                flag -= 1

            if self.ai.my_board.count_ship == 0:
                print('...')
                print('Ваша доска:')
                print(self.user.my_board.show_board())
                time.sleep(1)
                print('...')
                print('Доска компьютера:')
                print(self.ai.my_board.show_board())
                time.sleep(1)
                print('...')
                print('Вы победили!')
                break

            if self.user.my_board.count_ship == 0:
                print('...')
                print('Ваша доска:')
                print(self.user.my_board.show_board())
                time.sleep(1)
                print('...')
                print('Доска компьютера:')
                print(self.ai.my_board.show_board())
                time.sleep(1)
                print('...')
                print('Победа машины!')
                break
            flag += 1

    def start(self):  # Запуск игры
        self.greet()
        self.loop()
