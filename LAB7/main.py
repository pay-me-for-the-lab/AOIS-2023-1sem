import random

numWords, wordLen = 30, 8


def words_array():
    words = [[0] * wordLen for _ in range(numWords)]
    for i in range(numWords):
        for j in range(wordLen):
            words[i][j] = random.randint(0, 1)
    return words


def find(arr, attribute, g, l, j):
    g1 = calc_g(g, attribute[j], l, arr[j])
    l1 = calc_l(g, attribute[j], l, arr[j])
    if j == 0:
        return g1, l1
    else:
        return find(arr, attribute, g1, l1, j - 1)


def calc_g(g, a, l, s):
    if a == 0 and l == 0 and s == 1:
        return 1
    else:
        return g


def calc_l(g, a, l, s):
    if a == 1 and s == 0 and g == 0:
        return 1
    else:
        return l


def find_less(arr, attribute):
    g, l = 0, 0
    arr_less = []
    for i in range(len(arr)):
        g, l = find(arr[i], attribute, g, l, wordLen - 1)
        if g == 0 and l == 1:
            arr_less.append(arr[i])
        g, l = 0, 0
    if len(arr_less) == 0:
        return [0] * wordLen
    curr_biggest = arr_less[0]
    for i in range(len(arr_less)):
        g, l = 0, 0
        g, l = find(arr_less[i], curr_biggest, g, l, wordLen - 1)
        if g == 1 and l == 0:
            curr_biggest = arr_less[i]
    return curr_biggest


def find_more(arr, attribute):
    g, l = 0, 0
    arr_less = []
    for i in range(len(arr)):
        g, l = find(arr[i], attribute, g, l, wordLen - 1)
        if g == 1 and l == 0:
            arr_less.append(arr[i])
        g, l = 0, 0
    if len(arr_less) == 0:
        return [0] * wordLen
    curr_biggest = arr_less[0]
    for i in range(len(arr_less)):
        g, l = 0, 0
        g, l = find(arr_less[i], curr_biggest, g, l, wordLen - 1)
        if g == 0 and l == 1:
            curr_biggest = arr_less[i]
    return curr_biggest


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
        g_bottom, l_bottom = find(arr[i], top, g_top, l_top, wordLen - 1)
        g_top, l_top = find(arr[i], bottom, g_top, l_top, wordLen - 1)
        if g_top == 0 and l_top == 1:
            out_of_interval[i] = True
        if g_bottom == 1 and l_bottom == 0:
            out_of_interval[i] = True
        g_top, l_top, g_bottom, l_bottom = 0, 0, 0, 0
    return out_of_interval


def main():
    arr = words_array()
    for i in range(len(arr)):
        print(i, ": ", arr[i])
    find = arr[2]
    top = arr[5]
    bottom = arr[2]
    print("\nNearest-bottom:")
    print("Find ", find)
    print("Less ", find_less(arr, find))
    print("More ", find_more(arr, find))
    print("\nInterval:\nTop ", top, "  Bottom ", bottom)
    print("\nFounded interval:")
    interval = find_interval(arr, top, bottom)
    for i in range(len(interval)):
        print(interval[i])


if __name__ == "__main__":
    main()
