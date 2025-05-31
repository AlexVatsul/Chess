import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import random

# Создаем пустую доску 8x8
board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

def position(x):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == x:
                return i, j


# Устанавливаем фигуры: 1 - черный король, 2 - белый король, 3 - белая ладья

board[random.randint(0, 7)][random.randint(0, 7)] = 1  # Черный король
pos_1_i, pos_1_j = position(1)

lst_coords_1 = [
    (pos_1_i + 1, pos_1_j + 1),
    (pos_1_i - 1, pos_1_j + 1),
    (pos_1_i + 1, pos_1_j - 1),
    (pos_1_i - 1, pos_1_j - 1)
]


flag_3 = True
while flag_3:
    pos_3_i, pos_3_j = random.randint(0, 7), random.randint(0, 7)
    if pos_3_i == pos_1_i:
        continue
    elif pos_3_j == pos_1_j:
        continue
    elif (pos_3_i, pos_3_j) in lst_coords_1:
        continue
    else:
        flag_3 = False
        board[pos_3_i][pos_3_j] = 3

pos_3_i, pos_3_j = position(3)

lst_coords_2 = [
    (pos_1_i + 1, pos_1_j + 1),
    (pos_1_i - 1, pos_1_j + 1),
    (pos_1_i + 1, pos_1_j - 1),
    (pos_1_i - 1, pos_1_j - 1),
    (pos_1_i, pos_1_j + 1),
    (pos_1_i, pos_1_j - 1),
    (pos_1_i + 1, pos_1_j),
    (pos_1_i - 1, pos_1_j),
    (pos_1_i, pos_1_j),
    (pos_3_i, pos_3_j)
]


flag_2 = True
while flag_2:
    pos_2_i, pos_2_j = random.randint(0, 7), random.randint(0, 7)
    if (pos_2_i, pos_2_j) in lst_coords_2:
        continue
    else:
        flag_2 = False
        board[pos_2_i][pos_2_j] = 2


# board[3][0] = 1  # Черный король
# board[6][2] = 2  # Белый король
# board[7][1] = 3  # Белая ладья



root = tk.Tk()
root.title('Шахматная доска')

# Размер клетки
cell_size = 80

# Создаем холст для отображения доски
canvas = tk.Canvas(root, width=8 * cell_size, height=8 * cell_size)
canvas.pack()

# Словарь для хранения объектов PhotoImage
piece_images = {
    1: ImageTk.PhotoImage(Image.open("black_king.png").resize((cell_size, cell_size))),
    2: ImageTk.PhotoImage(Image.open("white_king.png").resize((cell_size, cell_size))),
    3: ImageTk.PhotoImage(Image.open("ladya_white.png").resize((cell_size, cell_size)))
}

# Создаем Label для отображения матрицы
matrix_label = tk.Label(root, text="", font=("Arial", 16))
matrix_label.pack()


def draw_board(board):
    canvas.delete("all")  # Очищаем холст перед каждым обновлением

    matrix_text = ""  # Текст для отображения матрицы

    for i in range(8):
        for j in range(8):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size

            # Отрисовываем клетку
            canvas.create_rectangle(x1, y1, x2, y2, fill="yellow" if (i + j) % 2 == 0 else "brown")

            # Отрисовываем фигуры
            piece_id = board[i][j]
            if piece_id in piece_images:
                img = piece_images[piece_id]
                canvas.create_image(x1, y1, anchor=tk.NW, image=img)

            matrix_text += str(board[i][j]) + " "  # Добавляем элемент матрицы к строке текста

        matrix_text += "\n"  # Переходим на следующую строку после завершения строки матрицы

    matrix_label.config(text=matrix_text)  # Обновляем текст в Label


# на вход координаты двух королей и ладьи
# на выход истина flag по горизонатли или вертикали, если ладья находится между королями, ложь, если нет
def king_or_king(i, j, i_l, j_l, i_k, j_k):
    # проверка на горизонталь
    flag = -1
    if (j_l > j or j_l > j_k) and (j_l < j or j_l < j_k):
        return True
    # проверка на вертикаль
    elif (i_l > i or i_l > i_k) and (i_l < i or i_l < i_k):
        return True
    return False

def kick_ladya(minimum, i_black, j_black, i_l, j_l, i_kwhite, j_kwhite):
    if minimum[1] == 1000:
        for i in minimum[0]:
            if sum((np.array([i_black, j_black]) - np.array([i, j_l])) ** 2) <= 2.0:
                return True
    elif minimum[1] == 2000:
        for j in minimum[0]:
            if sum((np.array([i_black, j_black]) - np.array([i_l, j])) ** 2) <= 2.0:
                return True


# функция на вход получает координаты всех точек
# на выходе нам нужно получить 2 списка значений по x и y с учетом взаимного расположения
def king_left_right_up_down(i_black, j_black, i_l, j_l, i_kwhite, j_kwhite):
    # проверка черный король слева от белого?
    x = []
    y = []
    if j_black < j_kwhite:
        if i_black > i_kwhite:
            x = [i for i in range((j_black + 1), j_kwhite)]
            y = [i for i in range((i_black - 1), i_kwhite, -1)]
        elif i_black < i_kwhite:
            x = [i for i in range((j_black + 1), j_kwhite)]
            y = [i for i in range((i_black + 1), i_kwhite)]
        elif i_black == i_kwhite:
            x = [i for i in range((j_black + 1), j_kwhite)]
            y = []
    elif j_black > j_kwhite:
        if i_black > i_kwhite:
            x = [i for i in range((j_kwhite + 1), j_black)]
            y = [i for i in range((i_kwhite + 1), i_black)]
        elif i_black < i_kwhite:
            x = [i for i in range((j_kwhite + 1), j_black)]
            y = [i for i in range((i_kwhite - 1), i_black, -1)]
        elif i_black == i_kwhite:
            x = [i for i in range((j_kwhite + 1), j_black)]
            y = []
    elif j_black == j_kwhite:
        if i_black > i_kwhite:
            x = []
            y = [i for i in range((i_kwhite + 1), i_black)]
        elif i_black < i_kwhite:
            x = []
            y = [i for i in range((i_kwhite - 1), i_black, -1)]
        elif i_black == i_kwhite:
            x = []
            y = []



    # найти минимальный по длине список
    minimum = []
    if x == []:
        minimum = (y, 1000)
    elif y == []:
        minimum = (x, 2000)
    elif i_kwhite == i_l:
        minimum = (y, 1000)
    elif j_kwhite == j_l:
        minimum = (x, 2000)

    elif len(x) > len(y):
        minimum = (y, 1000) # j_l - значит, что не меняется по x
    else:
        minimum = (x, 2000) # i_l - не меняется по y

    itog = -1
    if minimum[1] == 1000:
        for k in minimum[0]:
            if abs(k - i_black) == 1:
                if kick_ladya(minimum, i_black, j_black, i_l, j_l, i_kwhite, j_kwhite):
                    if x == []:
                        for t in minimum[0]:
                            if abs(t - i_black) == 2:
                                itog = t
                                break
                        return itog, j_l
                    else:
                        minimum = (x, 2000)
                        for t in minimum[0]:
                            if abs(t - j_black) == 1:
                                itog = t
                                break
                        return i_l, itog
                else:
                    itog = k
                    break
        return itog, j_l
    elif minimum[1] == 2000:
        for k in minimum[0]:
            if abs(k - j_black) == 1:
                if kick_ladya(minimum, i_black, j_black, i_l, j_l, i_kwhite, j_kwhite):
                    if y == []:
                        for t in minimum[0]:
                            if abs(t - j_black) == 2:
                                itog = t
                                break
                        return i_l, itog
                    else:
                        minimum = (y, 1000)
                        for t in minimum[0]:
                            if abs(t - i_black) == 1:
                                itog = t
                                break
                        return itog, j_l
                else:
                    itog = k
                    break
        return i_l, itog


# на вход координаты
# на выход обновленные координаты
def where_kings(i_black, j_black, i_l, j_l, i_kwhite, j_kwhite):

    new_i_l, new_j_l = i_l, j_l
    left, right, up, down = 1, 2, 3, 4
    storona = 0

    if j_black > j_kwhite:

        if i_black == i_kwhite:
            if sum((np.array([i_l, (j_black - 1)]) - np.array([i_black, j_black])) ** 2) > 2.0:
                new_j_l = j_black - 1
                storona = 2
            else:
                new_j_l = j_black - 2
                storona = 2

        elif i_black > i_kwhite:
            if abs(i_black - i_kwhite) > abs(j_black - j_kwhite):
                if sum((np.array([(i_black - 1), j_l]) - np.array([i_black, j_black])) ** 2) > 2.0:
                    new_i_l = i_black - 1
                    storona = 4
                else:
                    new_i_l = i_black - 2
                    storona = 4
            else:
                if sum((np.array([i_l, (j_black - 1)]) - np.array([i_black, j_black])) ** 2) > 2.0:
                    new_j_l = j_black - 1
                    storona = 2
                else:
                    new_j_l = j_black - 2
                    storona = 2

        elif i_kwhite > i_black:
            if abs(i_kwhite - i_black) > abs(j_kwhite - j_black):
                if sum((np.array([(i_black + 1), j_l]) - np.array([i_black, j_black])) ** 2) > 2.0:
                    new_i_l = i_black + 1
                    storona = 3
                else:
                    new_i_l = i_black + 2
                    storona = 3
            else:
                if sum((np.array([i_l, (j_black - 1)]) - np.array([i_black, j_black])) ** 2) > 2.0:
                    new_j_l = j_black - 1
                    storona = 2
                else:
                    new_j_l = j_black - 2
                    storona = 2

    elif j_kwhite > j_black:
        if i_black == i_kwhite:
            if sum((np.array([i_l, j_black + 1]) - np.array([i_black, j_black])) ** 2) > 2.0:
                new_j_l = j_black + 1
                storona = 1
            else:
                new_j_l = j_black + 2
                storona = 1

        elif i_black > i_kwhite:
            if abs(i_black - i_kwhite) > abs(j_black - j_kwhite):
                if sum((np.array([(i_black - 1), j_l]) - np.array([i_black, j_black])) ** 2) > 2.0:
                    new_i_l = i_black - 1
                    storona = 4
                else:
                    new_i_l = i_black - 2
                    storona = 4
            else:
                if sum((np.array([i_l, (j_black + 1)]) - np.array([i_black, j_black])) ** 2) > 2.0:
                    new_j_l = j_black + 1
                    storona = 1
                else:
                    new_j_l = j_black + 2
                    storona = 1

        elif i_kwhite > i_black:
            if abs(i_kwhite - i_black) > abs(j_kwhite - j_black):
                if sum((np.array([(i_black + 1), j_l]) - np.array([i_black, j_black])) ** 2) > 2.0:
                    new_i_l = i_black + 1
                    storona = 3
                else:
                    new_i_l = i_black + 2
                    storona = 3
            else:
                if sum((np.array([i_l, (j_black + 1)]) - np.array([i_black, j_black])) ** 2) > 2.0:
                    new_j_l = j_black + 1
                    storona = 1
                else:
                    new_j_l = j_black + 2
                    storona = 1

    return new_i_l, new_j_l, storona

def distance_between(i, j, i1, j1):
    dist = sum((np.array([i, j]) - np.array([i1, j1])) ** 2)
    return dist

def move_the_rook(i, j, i_l, j_l, storona):
    new_i_l, new_j_l = i_l, j_l
    if storona == 1:
        if abs(i - 0) >= abs(i - 7):
            new_i_l = 0
        else:
            new_i_l = 7
    elif storona == 2:
        if abs(i - 0) >= abs(i - 7):
            new_i_l = 0
        else:
            new_i_l = 7
    elif storona == 3:
        if abs(j - 0) >= abs(j - 7):
            new_j_l = 0
        else:
            new_j_l = 7
    elif storona == 4:
        if abs(j - 0) >= abs(j - 7):
            new_j_l = 0
        else:
            new_j_l = 7

    return new_i_l, new_j_l



storona = 0
def strategy_place():
    global storona

    i, j = position(1)
    i_l, j_l = position(3)
    i_k, j_k = position(2)
    new_i, new_j = i_l, j_l
    t = 0

    # начальный сдвиг ладьи на оптимальное расстояние в одну клетку без удара
    if storona == 0:
        if king_or_king(i, j, i_l, j_l, i_k, j_k) == False:
            new_i, new_j = king_left_right_up_down(i, j, i_l, j_l, i_k, j_k)
            if new_i > i_l:
                # движение вниз
                storona = 4
            elif i_l > new_i:
                # движение вверх
                storona = 3
            elif new_j > j_l:
                # движение вправо
                storona = 2
            elif j_l > new_j:
                # движение влево
                storona = 1
            board[i_l][j_l] = 0
            board[new_i][new_j] = 3
            t = 1
            draw_board(board)
            return None
        elif king_or_king(i, j, i_l, j_l, i_k, j_k) == True:
            new_i, new_j, storona = where_kings(i, j, i_l, j_l, i_k, j_k)
            board[i_l][j_l] = 0
            board[new_i][new_j] = 3
            t = 1
            draw_board(board)
            return None



    # left, right, up, down = 1, 2, 3, 4


    # движение ладьи
    if storona == 1:
        print(storona, "влево")
        if distance_between(i, j, i_l, j_l) <= 2:
            new_i_l, new_j_l = move_the_rook(i, j, i_l, j_l, storona)
            board[i_l][j_l] = 0
            board[new_i_l][new_j_l] = 3
            t = 1
        elif abs(j - new_j) > 1.0:
            board[new_i][new_j] = 0
            board[new_i][new_j - 1] = 3
            t = 1
    elif storona == 2:
        print(storona, "вправо")
        if distance_between(i, j, i_l, j_l) <= 2:
            new_i_l, new_j_l = move_the_rook(i, j, i_l, j_l, storona)
            board[i_l][j_l] = 0
            board[new_i_l][new_j_l] = 3
            t = 1
        elif abs(j - new_j) > 1.0:
            board[new_i][new_j] = 0
            board[new_i][new_j + 1] = 3
            t = 1
    elif storona == 3:
        print(storona, "вверх")
        if distance_between(i, j, i_l, j_l) <= 2:
            new_i_l, new_j_l = move_the_rook(i, j, i_l, j_l, storona)
            board[i_l][j_l] = 0
            board[new_i_l][new_j_l] = 3
            t = 1
        elif abs(i - new_i) > 1.0:
            board[new_i][new_j] = 0
            board[new_i - 1][new_j] = 3
            t = 1
    elif storona == 4:
        print(storona, "вниз")
        if distance_between(i, j, i_l, j_l) <= 2:
            new_i_l, new_j_l = move_the_rook(i, j, i_l, j_l, storona)
            board[i_l][j_l] = 0
            board[new_i_l][new_j_l] = 3
            t = 1
        elif abs(i - new_i) > 1.0:
            board[new_i][new_j] = 0
            board[new_i + 1][new_j] = 3
            t = 1

    i, j = position(1)
    i_l, j_l = position(3)
    i_k, j_k = position(2)

    # движение короля

    # влево
    if storona == 1 and t == 0:
        if abs(j_l - j_k) > 1.0:
            board[i_k][j_k] = 0
            board[i_k][j_k - 1] = 2
        elif abs(j_l - j_k) == 1.0:
            if abs((i_k + 1) - i) > abs((i_k - 1) - i):
                if (i_k) == i:
                    board[i_l][j_l] = 0
                    board[i_l][j_l - 1] = 3
                elif (i_k - 1) == i:
                    if  (0 <= (i_k + 2)) and (7 >= (i_k + 2)):
                        board[i_l][j_l] = 0
                        board[i_k + 2][j_l] = 3
                    else:
                        board[i_k][j_k] = 0
                        board[i_k - 1][j_k] = 2
                else:
                    board[i_k][j_k] = 0
                    board[i_k - 1][j_k] = 2
            else:
                if (i_k) == i:
                    board[i_l][j_l] = 0
                    board[i_l][j_l - 1] = 3
                elif (i_k + 1) == i:
                    if (0 <= (i_k - 2)) and (7 >= (i_k - 2)):
                        board[i_l][j_l] = 0
                        board[i_k - 2][j_l] = 3
                    else:
                        board[i_k][j_k] = 0
                        board[i_k + 1][j_k] = 2
                else:
                    board[i_k][j_k] = 0
                    board[i_k + 1][j_k] = 2

    # вправо
    elif storona == 2 and t == 0:
        if abs(j_l - j_k) > 1.0:
            board[i_k][j_k] = 0
            board[i_k][j_k + 1] = 2
        elif abs(j_l - j_k) == 1.0:
            if abs((i_k + 1) - i) > abs((i_k - 1) - i):
                if (i_k) == i:
                    board[i_l][j_l] = 0
                    board[i_l][j_l + 1] = 3
                elif (i_k - 1) == i:
                    if (0 <= (i_k + 2)) and (7 >= (i_k + 2)):
                        board[i_l][j_l] = 0
                        board[i_k + 2][j_l] = 3
                    else:
                        board[i_k][j_k] = 0
                        board[i_k - 1][j_k] = 2
                else:
                    board[i_k][j_k] = 0
                    board[i_k - 1][j_k] = 2
            else:
                if (i_k) == i:
                    board[i_l][j_l] = 0
                    board[i_l][j_l + 1] = 3
                elif (i_k + 1) == i:
                    if (0 <= (i_k - 2)) and (7 >= (i_k - 2)):
                        board[i_l][j_l] = 0
                        board[i_k - 2][j_l] = 3
                    else:
                        board[i_k][j_k] = 0
                        board[i_k + 1][j_k] = 2
                else:
                    board[i_k][j_k] = 0
                    board[i_k + 1][j_k] = 2

    # вверх
    elif storona == 3 and t == 0:
        if abs(i_l - i_k) > 1.0:
            board[i_k][j_k] = 0
            board[i_k - 1][j_k] = 2
        elif abs(i_l - i_k) == 1.0:
            if abs((j_k + 1) - j) > abs((j_k - 1) - j):
                if (j_k) == j:
                    board[i_l][j_l] = 0
                    board[i_l - 1][j_l] = 3
                elif (j_k - 1) == j:
                    if (0 <= (j_k + 2)) and (7 >= (j_k + 2)):
                        board[i_l][j_l] = 0
                        board[i_l][j_k + 2] = 3
                    else:
                        board[i_k][j_k] = 0
                        board[i_k][j_k - 1] = 2
                else:
                    board[i_k][j_k] = 0
                    board[i_k][j_k - 1] = 2
            else:
                if (j_k) == j:
                    board[i_l][j_l] = 0
                    board[i_l - 1][j_l] = 3
                elif (j_k + 1) == j:
                    if (0 <= (j_k - 2)) and (7 >= (j_k - 2)):
                        board[i_l][j_l] = 0
                        board[i_l][j_k - 2] = 3
                    else:
                        board[i_k][j_k] = 0
                        board[i_k][j_k + 1] = 2
                else:
                    board[i_k][j_k] = 0
                    board[i_k][j_k + 1] = 2

    # вниз
    elif storona == 4 and t == 0:
        if abs(i_l - i_k) > 1.0:
            board[i_k][j_k] = 0
            board[i_k + 1][j_k] = 2
        elif abs(i_l - i_k) == 1.0:
            if abs((j_k + 1) - j) > abs((j_k - 1) - j):
                if (j_k) == j:
                    board[i_l][j_l] = 0
                    board[i_l + 1][j_l] = 3
                elif (j_k - 1) == j:
                    if (0 <= (j_k + 2)) and (7 >= (j_k + 2)):
                        board[i_l][j_l] = 0
                        board[i_l][j_k + 2] = 3
                    else:
                        board[i_k][j_k] = 0
                        board[i_k][j_k - 1] = 2
                else:
                    board[i_k][j_k] = 0
                    board[i_k][j_k - 1] = 2
            else:
                if (j_k) == j:
                    board[i_l][j_l] = 0
                    board[i_l + 1][j_l] = 3
                elif (j_k + 1) == j:
                    if (0 <= (j_k - 2)) and (7 >= (j_k - 2)):
                        board[i_l][j_l] = 0
                        board[i_l][j_k - 2] = 3
                    else:
                        board[i_k][j_k] = 0
                        board[i_k][j_k + 1] = 2
                else:
                    board[i_k][j_k] = 0
                    board[i_k][j_k + 1] = 2

    draw_board(board)



def is_valid_move(i, j, i_l, j_l, i_k, j_k):
    return ((i < 7 and (i + 1) != i_l and j_l != j and sum((np.array([i, j]) - np.array([i_k - 1, j_k])) ** 2) > 2.0) or
            (i > 0 and (i - 1) != i_l and j_l != j and sum((np.array([i, j]) - np.array([i_k + 1, j_k])) ** 2) > 2.0) or
            (j < 7 and (j + 1) != j_l and i_l != i and sum((np.array([i, j]) - np.array([i_k, j_k - 1])) ** 2) > 2.0) or
            (j > 0 and (j - 1) != j_l and i_l != i and sum((np.array([i, j]) - np.array([i_k, j_k + 1])) ** 2) > 2.0) or
            (i > 0 and j > 0 and (j - 1) != j_l and (i - 1) != i_l and sum(
                (np.array([i, j]) - np.array([i_k + 1, j_k + 1])) ** 2) > 2.0) or
            (i < 7 and j < 7 and (j + 1) != j_l and (i + 1) != i_l and sum(
                (np.array([i, j]) - np.array([i_k - 1, j_k - 1])) ** 2) > 2.0) or
            (i > 0 and j < 7 and (j + 1) != j_l and (i - 1) != i_l and sum(
                (np.array([i, j]) - np.array([i_k + 1, j_k - 1])) ** 2) > 2.0) or
            (i < 7 and j > 0 and (j - 1) != j_l and (i + 1) != i_l and sum(
                (np.array([i, j]) - np.array([i_k - 1, j_k + 1])) ** 2) > 2.0)
            )


def proverka_key(key, i, j, i_l, j_l, i_k, j_k):
    if key == 'x':
        return (i < 7 and (i + 1) != i_l and j_l != j and sum((np.array([i, j]) - np.array([i_k - 1, j_k])) ** 2) > 2.0)
    elif key == 'w':
        return (i > 0 and (i - 1) != i_l and j_l != j and sum((np.array([i, j]) - np.array([i_k + 1, j_k])) ** 2) > 2.0)
    elif key == 'd':
        return (j < 7 and (j + 1) != j_l and i_l != i and sum((np.array([i, j]) - np.array([i_k, j_k - 1])) ** 2) > 2.0)
    elif key == 'a':
        return (j > 0 and (j - 1) != j_l and i_l != i and sum((np.array([i, j]) - np.array([i_k, j_k + 1])) ** 2) > 2.0)
    elif key == 'q':
        return (i > 0 and j > 0 and (j - 1) != j_l and (i - 1) != i_l and sum(
            (np.array([i, j]) - np.array([i_k + 1, j_k + 1])) ** 2) > 2.0)
    elif key == 'c':
        return (i < 7 and j < 7 and (j + 1) != j_l and (i + 1) != i_l and sum(
            (np.array([i, j]) - np.array([i_k - 1, j_k - 1])) ** 2) > 2.0)
    elif key == 'e':
        return (i > 0 and j < 7 and (j + 1) != j_l and (i - 1) != i_l and sum(
            (np.array([i, j]) - np.array([i_k + 1, j_k - 1])) ** 2) > 2.0)
    elif key == 'z':
        return (i < 7 and j > 0 and (j - 1) != j_l and (i + 1) != i_l and sum(
            (np.array([i, j]) - np.array([i_k - 1, j_k + 1])) ** 2) > 2.0)


def show_loss_screen():
    canvas.delete("all")  # Очищаем холст перед отображением проигрышного экрана
    canvas.create_rectangle(0, 0, 8 * cell_size, 8 * cell_size, fill="white")
    canvas.create_text(4 * cell_size, 4 * cell_size, text="Вы проиграли", font=("Arial", 20), fill="red")

storona_itog = 0
def move_black_king_key(event):
    key = event.keysym
    print("Клавиша нажата:", key)

    i, j = position(1)
    i_l, j_l = position(3)
    i_k, j_k = position(2)

    new_i, new_j = i, j

    if key == 'x':
        new_i += 1
    elif key == 'w':
        new_i -= 1
    elif key == 'd':
        new_j += 1
    elif key == 'a':
        new_j -= 1
    elif key == 'q':
        new_i, new_j = i - 1, j - 1
    elif key == 'c':
        new_i, new_j = i + 1, j + 1
    elif key == 'e':
        new_i, new_j = i - 1, j + 1
    elif key == 'z':
        new_i, new_j = i + 1, j - 1
    else:
        print("Введите нужную клавишу для перемещения короля")

    if is_valid_move(i, j, i_l, j_l, i_k, j_k):
        if proverka_key(key, i, j, i_l, j_l, i_k, j_k):
            board[i][j] = 0
            board[new_i][new_j] = 1
            draw_board(board)
            strategy_place()
        else:
            print("Недопустимый ход")
    else:
        print("Вы проиграли")
        show_loss_screen()


# Привязываем функцию к событиям клавиатуры
root.bind("<Key>", move_black_king_key)

# Привязываем функцию к событиям клавиатуры
root.bind("<Key>", move_black_king_key)

draw_board(board)
root.mainloop()
