# Файл для тестирования функционала проекта
from main import *

# Проверка класса Dot
dot1 = Dot(1, 3)
dot2 = Dot(2, 4)
dot3 = Dot(1, 3)

print(dot1 == dot2)
print(dot1 == dot3)
print(f'Точка 1: {dot1}, Точка 2: {dot2}, Точка 3: {dot3}')
