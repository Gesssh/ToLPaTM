#Вариант 1.
# На вход программы подается описание переменных на выбранном языке (Pascal, C++, C# и т.д.).
# Программа должна проанализировать его при помощи ДКА или ДМПА и выдать результат проверки.
# Это может быть:
#   1. Сообщение о том, что описание корректное.
#   2. Сообщение о синтаксической ошибке. Указывать тип ошибки не обязательно,
#       требуется только указать строку и позицию в строке входного файла,
#       где наблюдается ошибка. Достаточно находить только первую ошибку в описании.
#   3. Сообщение о дублировании имен переменных.
#   В этом случае на выходе программы необходимо указать имя дублируемой переменной,
#   а также строку и позицию в строке, где встретился дубликат.
# При этом программа может быть написана на одном языке программирования,
# но проверять правильность описания переменных на другом языке.

def main():
    global q
    global start_chain # начальное положение цепочки
    global chain_now # положение цепочки
    global type_num
    global buffer
    global first_array
    global data_lex
    global data_x

    file = open('input.txt')
    line_count= 1
    pos = 1
    for line in file:

        for symbol in line:
            if symbol == '\n':
                pass
            else:
                value = alphabet[str(symbol)]
                action_index = status_table[value][q][0] # получение номера action

                if action_index == 0: # ожидание
                    chain_now += 1

                elif action_index == 1: # добавление символа в буфер
                    buffer += symbol
                    chain_now += 1

                elif action_index == 2:# проверка var
                    if buffer in data_lex:
                        buffer = ""
                        start_chain = chain_now
                    else:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()

                elif action_index == 3:# проверка типа данных
                    chain_now += 1
                    if buffer in data_type:
                        type_num = data_type.index(buffer)
                        buffer = ""
                        start_chain = chain_now
                    else:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()

                elif action_index == 4:# проверка переменной на соответствие системной
                    if buffer in data_type:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()
                    if buffer in data_lex:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()
                    if buffer in data_x:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()
                    data_x.append(buffer)
                    buffer = ''
                    start_chain = chain_now

                elif action_index == 5:# проверка соответствие числа в [] и типа данных
                    if type_num == -1:
                        chain_now += 1
                        if buffer in data_type:
                            type_num = data_type.index(buffer)
                            buffer = ""
                            start_chain = chain_now
                        else:
                            print("Error line", line_count, 'pos', chain_now)
                            exit()

                    if type_num >= 4:
                        buffer =''
                        start_chain = chain_now
                    else:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()

                elif action_index == 6:# переход на новую строку после полного обьявления
                    start_chain = 1
                    chain_now = 1
                    buffer = ''
                    type_num = -1

                elif action_index == 7:# запомнить первое число индекса
                    if type_num != 5:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()
                    chain_now += 1
                    first_array = int(buffer)
                    buffer = ''

                elif action_index == 8:# сброс типа
                    chain_now += 1
                    if type_num == 4:
                        if (int(buffer)<= 0 or int(buffer) > 255):
                            print("Error line", line_count, 'pos', chain_now)
                            exit()

                    start_chain = chain_now
                    type_num = -1
                    if symbol == ';':
                        start_chain = 1
                        chain_now = 1
                        buffer = ''
                        type_num = -1

                elif action_index == 9:# проверка of
                    chain_now += 1
                    if buffer in data_lex:
                        start_chain = chain_now
                        buffer = ''
                    else:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()

                elif action_index == 10:# проверка индексов
                    chain_now += 1
                    if first_array <= int(buffer):
                        buffer = ''
                        start_chain = chain_now
                    else:
                        print("Error line", line_count, 'pos', chain_now)
                        exit()

                elif action_index == 11:# сброс типа и запись в бефер после array[]
                    chain_now += 1
                    start_chain = chain_now
                    type_num = -1
                    buffer += symbol

                else:
                    print("Error line", line_count, 'pos', chain_now)
                    exit()


                q = status_table[value][q][1] # получение номера следующего состояния
                if (q == -1):# -1 состояние ошибки
                    print("Error line", line_count, 'pos', chain_now)
                    exit()
        line_count += 1



q = 0 # состояние автомата
data_type = ["integer", "real", "boolean", "char", "string", "array"] #тип ыданных
data_lex = ["var", "of"] # лексемы
data_x = []# переменные
data_index = [] # индекс переменых

type_num = -7 # хранит тип данных
first_array  = 0# первый индекс
buffer = ""
start_chain = 1# начальное положение цепочки
chain_now = 1# положение цепочки


alphabet ={
    'A': 0,     'a': 0,     '_': 0,
    'B': 0,     'b': 0,     '0': 1,
    'C': 0,     'c': 0,     '1': 1,
    'D': 0,     'd': 0,     '2': 1,
    'E': 0,     'e': 0,     '3': 1,
    'F': 0,     'f': 0,     '4': 1,
    'G': 0,     'g': 0,     '5': 1,
    'H': 0,     'h': 0,     '6': 1,
    'I': 0,     'i': 0,     '7': 1,
    'J': 0,     'j': 0,     '8': 1,
    'K': 0,     'k': 0,     '9': 1,
    'L': 0,     'l': 0,     ':': 2,
    'M': 0,     'm': 0,     ';': 3,
    'N': 0,     'n': 0,     ' ': 4,
    'O': 0,     'o': 0,     '\t': 4,
    'P': 0,     'p': 0,     ',': 5,
    'Q': 0,     'q': 0,     '.': 6,
    'R': 0,     'r': 0,     '[': 7,
    'S': 0,     's': 0,     ']': 8,
    'T': 0,     't': 0,     '-': 9,
    'U': 0,     'u': 0,
    'V': 0,     'v': 0,
    'W': 0,     'w': 0,
    'X': 0,     'x': 0,
    'Y': 0,     'y': 0,
    'Z': 0,     'z': 0,
}

status_table = [
#   0      1         2       3        4        5       6       7       8         9       10      11      12      13      14      15       16      17      18       19      20
[[1, 1], [1, 1],  [1, 2],  [1, 4],  [1, 4],  [0,-1], [0,-1], [0,-1], [11, 9], [1, 9],  [0,-1], [0,-1], [0,-1], [0,-1], [0,-1], [1, 2],  [0,-1], [0,-1], [1, 9],  [0,-1], [1, 2]],  # _a-z (0)
[[0,-1], [0,-1],  [0,-1],  [0,-1],  [1, 4],  [1, 5], [0,-1], [0,-1], [0,-1],  [0,-1],  [0,-1], [1,12], [1,12], [1,14], [1,14], [0,-1],  [1, 5], [0,-1], [0,-1],  [0,-1], [0,-1]],  # 0-9  (1)
[[0,-1], [0,-1],  [0,-1],  [0,-1],  [4,15],  [0,-1], [0,-1], [0,-1], [0,-1],  [0,-1],  [0,-1], [0,-1], [0,-1], [0,-1], [0,-1], [0,-1],  [0,-1], [0,-1], [0,-1],  [0,15], [0,-1]],  # :    (2)
[[0,-1], [0,-1],  [3, 3],  [0,-1],  [0,-1],  [0,-1], [6, 3], [8, 3], [0,-1],  [0,-1],  [0,-1], [0,-1], [0,-1], [0,-1], [0,-1], [0,-1],  [0,-1], [0, 3], [0,-1],  [0,-1], [0, 3]],  # ;    (3)
[[0,-1], [2, 3],  [3, 6],  [0, 3],  [4, 4],  [0,-1], [0, 6], [0, 7], [0, 8],  [9,15],  [0,-1], [0,-1], [0,-1], [0,13], [0,-1], [0,15],  [0,16], [0,17], [0,18],  [0,19], [0,20]],  # " "  (4)
[[0,-1], [0,-1],  [0,-1],  [0,-1],  [4, 3],  [0,-1], [0,-1], [0,-1], [0,-1],  [0,-1],  [0,-1], [0,-1], [10,13],[0,-1], [0,-1], [0,-1],  [0,-1], [0,-1], [0,-1],  [4, 3], [0,-1]],  # ,    (5)
[[0,-1], [0,-1],  [0,-1],  [0,-1],  [0,-1],  [7,10], [0,-1], [0,-1], [0,-1],  [0,-1],  [0,11], [0,-1], [0,-1], [0,-1], [7,10], [0,-1],  [0,-1], [0,-1], [0,-1],  [0,-1], [0,-1]],  # .    (6)
[[0,-1], [0,-1],  [5,16],  [0,-1],  [0,-1],  [0,-1], [5,16], [0,-1], [0,-1],  [0,-1],  [0,-1], [0,-1], [0,-1], [0,-1], [0,-1], [0,-1],  [0,-1], [0,-1], [0,-1],  [0,-1], [0,-1]],  # [    (7)
[[0,-1], [0,-1],  [0,-1],  [0,-1],  [0,-1],  [8, 7], [0,-1], [0,-1], [0,-1],  [0,-1],  [0,-1], [0,-1], [10, 8],[0,-1], [0,-1], [0,-1],  [0,-1], [0,-1], [0,-1],  [0,-1], [0,-1]],  # ]    (8)
[[0,-1], [0,-1],  [0,-1],  [0,-1],  [1, 4],  [0,-1], [0,-1], [0,-1], [0,-1],  [0,-1],  [0,-1], [1,12], [0,-1], [1,14], [0,-1], [0,-1],  [1, 5], [0,-1], [0,-1],  [0,-1], [0,-1]],  # -    (9)
[[0, 0], [2, 3],  [3,17],  [0, 3],  [4,19],  [0, 5], [0, 6], [0,17], [0,18],  [9,15],  [0,-1], [0,11], [10,12],[0,13], [0,14], [0,20],  [0,16], [0,17], [0,18],  [0,19], [0,20]] # \0   (10)
]

# 0 начальный
# 1 командная перменная
# 2 тип данных тело
# 3 переменная первый символ
# 4 переменная тело
# 5 string[...
# 6 тип...
# 7 string[]...
# 8 array[]...
# 9  of
# 10 array[1.
# 11 array[1..
# 12 array[1..2
# 13 array[1..2,
# 14 array[1..2, 3
# 15 тип данных первый символ
# 16 [...
# 17 ожидание ;
# 18 ожидане of
# 19 ожидание , или :
# 20 ожидание типа

if __name__ == '__main__':
    main()