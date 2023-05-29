from Memory import Memory


def main():
    memory = Memory()
    memory.write(15, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    memory.print()
    print("Sorted by descending: ")
    memory.sort(True)
    memory.print()
    V = [0, 1, 1]
    memory.sum(V)
    print(f"Memory after sum:{V}")
    memory.print()
    print(f"Reading line 12: {memory.readLine(12)}")
    print(
        f"function_4 for words 0x00 and 0x01 in 0x02:\n{memory.read(0)}\n{memory.read(1)}\n{memory.read(2)}"
    )
    print(
        f"function_6 for words 0x03 and 0x04 in 0x05:\n{memory.read(3)}\n{memory.read(4)}\n{memory.read(5)}"
    )
    print(
        f"function_9 for words 0x06 and 0x07 in 0x08:\n{memory.read(6)}\n{memory.read(7)}\n{memory.read(8)}"
    )
    print(
        f"function_11 for words 0x09 and 0x10 in 0x11:\n{memory.read(9)}\n{memory.read(10)}\n{memory.read(11)}"
    )
    memory.function_4(0, 1, 2)
    memory.function_6(3, 4, 5)
    memory.function_9(6, 7, 8)
    memory.function_11(9, 10, 11)


if __name__ == "__main__":
    main()
