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


def find_less(words, choosen):
    g, l = 0, 0
    words_less = []
    for i in range(len(words)):
        g, l = find(words[i], choosen, g, l, word_len - 1)
        if g == 0 and l == 1:
            words_less.append(words[i])
        g, l = 0, 0
    if len(words_less) == 0:
        return [0] * word_len
    curr_biggest = words_less[0]
    for i in range(len(words_less)):
        g, l = 0, 0
        g, l = find(words_less[i], curr_biggest, g, l, word_len - 1)
        if g == 1 and l == 0:
            curr_biggest = words_less[i]
    return curr_biggest


def find_more(words, choosen):
    g, l = 0, 0
    words_less = []
    for i in range(len(words)):
        g, l = find(words[i], choosen, g, l, word_len - 1)
        if g == 1 and l == 0:
            words_less.append(words[i])
        g, l = 0, 0
    if len(words_less) == 0:
        return [0] * word_len
    curr_biggest = words_less[0]
    for i in range(len(words_less)):
        g, l = 0, 0
        g, l = find(words_less[i], curr_biggest, g, l, word_len - 1)
        if g == 0 and l == 1:
            curr_biggest = words_less[i]
    return curr_biggest


def find_interval(words, top, bottom):
    interval = []
    out_of_interval = find_out_of_interval(words, top, bottom)
    for i in range(len(words)):
        if not out_of_interval[i]:
            interval.append(words[i])
    return interval


def find_out_of_interval(words, top, bottom):
    g_top, l_top, g_bottom, l_bottom = 0, 0, 0, 0
    out_of_interval = [False] * len(words)
    for i in range(len(words)):
        g_bottom, l_bottom = find(words[i], top, g_top, l_top, word_len - 1)
        g_top, l_top = find(words[i], bottom, g_top, l_top, word_len - 1)
        if g_top == 0 and l_top == 1:
            out_of_interval[i] = True
        if g_bottom == 1 and l_bottom == 0:
            out_of_interval[i] = True
        g_top, l_top, g_bottom, l_bottom = 0, 0, 0, 0
    return out_of_interval


def main():
    words = words_wordsay()
    print("\nСловарь:")
    for i in range(len(words)):
        print(words[i])
    choosen = words[5]
    start = words[2]
    end = words[9]
    print("\nПоиск ближайшего сверху и снизу значения:")
    print("Выбранное слово", choosen)
    print("Снизу", find_less(words, choosen))
    print("Сверху", find_more(words, choosen))
    print("\nИнтервал:\nОт", start, "\nДо", end)
    print("\nНайденные слова на интервале:")
    interval = find_interval(words, start, end)
    for i in range(len(interval)):
        print(interval[i])


if __name__ == "__main__":
    main()
