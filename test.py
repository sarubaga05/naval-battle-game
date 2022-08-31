# Файл для тестирования функционала проекта
from main import *

# Проверка класса Dot
'''
dot1 = Dot(1, 3)
dot2 = Dot(2, 4)
dot3 = Dot(1, 3)

print(dot1 == dot2)
print(dot1 == dot3)
print(f'Точка 1: {dot1}, Точка 2: {dot2}, Точка 3: {dot3}')
'''

# Проверка класса Ship
'''
dot1 = Dot(1, 1)
dot2 = Dot(3, 4)
ship1 = Ship(3, dot1, 1)
ship1 = ship1.dots
ship2 = Ship(2, dot2, 0)
ship2 = ship2.dots
for d in ship1:
    print(d)
print()
for d in ship2:
    print(d)
'''

# Проверка класса Board
'''
dot1 = Dot(1, 1)
dot2 = Dot(2, 1)
dot3 = Dot(6, 6)
ship1 = Ship(2, dot2, 1)
board1 = Board()
# Вывод доски
#print(board1.show_board())
# Добавление корабля
#board1.add_ship(ship1)
#board1.clean_used_dots()
#board1.contour(ship1, True)
#print(board1.show_board())
#board1.hid = True
#print(board1.show_board())
# Проверка выхода за границу
#print(board1.out(dot3))
# Проверка выстрела
#board1.add_ship(ship1)
#board1.clean_used_dots()
#print(board1.shot(dot2))
#print(board1.show_board())
#print(board1.shot(dot1))
#print(board1.show_board())
#print(board1.shot(dot3))
'''

# Проверка классов Player, AI, User
'''
board1 = Board()
board2 = Board()
ai1 = AI(board2, board1)
user1 = User(board1, board2)
#print(ai1.ask())
#print(user1.ask())
#print(ai1.move())
print(user1.move())
'''

