import random

num_words, word_len = 11, 8


def words_wordsay():
    words = [[0] * word_len for _ in range(num_words)]
    for i in range(num_words):
        for j in range(word_len):
            words[i][j] = random.randint(0, 1)
    return words


def find(words, choosen, g, l, j):
    g1 = calculate_g(g, choosen[j], l, words[j])
    l1 = calculate_l(g, choosen[j], l, words[j])
    if j == 0:
        return g1, l1
    else:
        return find(words, choosen, g1, l1, j - 1)


def calculate_g(g, a, l, s):
    if a == 0 and l == 0 and s == 1:
        return 1
    else:
        return g


def calculate_l(g, a, l, s):
    if a == 1 and s == 0 and g == 0:
        return 1
    else:
        return l


def find_less(arr, attribute):
    g, l = 0, 0
    arr_less = []
    for i in range(len(arr)):
        g, l = find(arr[i], attribute, g, l, word_len - 1)
        if g == 0 and l == 1:
            arr_less.append(arr[i])
        g, l = 0, 0
    if len(arr_less) == 0:
        return [0] * word_len
    curr_biggest = arr_less[0]
    for i in range(len(arr_less)):
        g, l = 0, 0
        g, l = find(arr_less[i], curr_biggest, g, l, word_len - 1)
        if g == 1 and l == 0:
            curr_biggest = arr_less[i]
    return curr_biggest


def find_more(arr, attribute):
    g, l = 0, 0
    arr_more = []
    for i in range(len(arr)):
        g, l = find(arr[i], attribute, g, l, word_len - 1)
        if g == 1 and l == 0:
            arr_more.append(arr[i])
        g, l = 0, 0
    if len(arr_more) == 0:
        return [0] * word_len
    curr_biggest = arr_more[0]
    for i in range(len(arr_more)):
        g, l = 0, 0
        g, l = find(arr_more[i], curr_biggest, g, l, word_len - 1)
        if g == 0 and l == 1:
            curr_biggest = arr_more[i]
    return curr_biggest


def binary_to_decimal(binary_list):
    binary_list.reverse()
    decimal = 0
    for digit in binary_list:
        decimal = decimal * 2 + digit
    binary_list.reverse()
    return decimal


def find_interval(arr, top, bottom):
    interval = []
    out_of_interval = find_out_of_interval(arr, top, bottom)
    for i in range(len(arr)):
        if not out_of_interval[i]:
            interval.append(arr[i])
    return interval


def find_out_of_interval(arr, top, bottom):
    g_top, l_top, g_bottom, l_bottom = 0, 0, 0, 0
    out_of_interval = [False] * len(arr)
    for i in range(len(arr)):
        g_bottom, l_bottom = find(arr[i], top, g_top, l_top, word_len - 1)
        g_top, l_top = find(arr[i], bottom, g_top, l_top, word_len - 1)
        if g_top == 0 and l_top == 1:
            out_of_interval[i] = True
        if g_bottom == 1 and l_bottom == 0:
            out_of_interval[i] = True
        g_top, l_top, g_bottom, l_bottom = 0, 0, 0, 0
    return out_of_interval


def main():
    random.seed(13)
    words = words_wordsay()
    print("\nСловарь:")
    for i in range(len(words)):
        print(str(words[i]) + " -> " + str(binary_to_decimal(words[i])))
    choosen = words[6]
    start = words[4]
    end = words[9]
    print("\nПоиск ближайшего сверху и снизу значения:")
    print("Выбранное слово", str(choosen) + " -> " + str(binary_to_decimal(choosen)))
    print("Снизу", str(find_less(words, choosen)) + " -> " + str(binary_to_decimal(find_less(words, choosen))))
    print("Сверху", str(find_more(words, choosen)) + " -> " + str(binary_to_decimal(find_more(words, choosen))))
    print("\nИнтервал:\nОт", str(start) + " -> " + str(binary_to_decimal(start)) + "\nДо", str(end) + " -> "
          + str(binary_to_decimal(end)))
    print("\nНайденные слова на интервале:")
    interval = find_interval(words, end, start)
    for i in range(len(interval)):
        print(str(interval[i]) + " -> " + str(binary_to_decimal(interval[i])))


if __name__ == "__main__":
    main()
