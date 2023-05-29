import random as rn


class Memory:
    def __init__(self):
        self.__memory = []
        self.__normal_view = []
        for i in range(16):
            row = []
            for j in range(16):
                row.append(rn.randint(0, 1))
            self.__memory.append(row)
        for i in range(16):
            self.__normal_view.append(self.read(i))

    def function_4(self, address_1, address_2, address_3):
        word_1 = self.read(address_1)
        word_2 = self.read(address_2)
        word_3 = []
        for i in range(16):
            word_3.append(1) if (word_1[i] == 0 and word_2[i] == 1) else word_3.append(
                0
            )
        self.write(address_3, word_3)

    def function_6(self, address_1, address_2, address_3):
        word_1 = self.read(address_1)
        word_2 = self.read(address_2)
        word_3 = []
        for i in range(16):
            word_3.append(1) if (word_1[i] != word_2[i]) else word_3.append(0)
        self.write(address_3, word_3)

    def function_9(self, address_1, address_2, address_3):
        word_1 = self.read(address_1)
        word_2 = self.read(address_2)
        word_3 = []
        for i in range(16):
            word_3.append(1) if (word_1[i] == word_2[i]) else word_3.append(0)
        self.write(address_3, word_3)

    def function_11(self, address_1, address_2, address_3):
        word_1 = self.read(address_1)
        word_2 = self.read(address_2)
        word_3 = []
        for i in range(16):
            word_3.append(0) if (word_1[i] == 0 and word_2[i] == 1) else word_3.append(
                1
            )
        self.write(address_3, word_3)

    def sort(self, descending):
        for i in range(16):
            for j in range(15 - i):
                if self.greater(self.read(j), self.read(j + 1)):
                    word_copy = self.read(j)
                    self.write(j, self.read(j + 1))
                    self.write(j + 1, word_copy)
        if descending:
            self.normalView()
            self.__normal_view = self.__normal_view[::-1]
            self.diagonalView()

    def sum(self, V):
        print(f"\nFinded words for V = {V}:")
        for i in range(16):
            if self.__normal_view[i][0:3] == V:
                print(self.__normal_view[i])
                self.__normal_view[i][11:16] = self.sumBinaries(
                    self.__normal_view[i][3:16]
                )
                print(self.__normal_view[i][11:16])
                print(self.__normal_view[i])
            self.write(i, self.__normal_view[i])

    def sumBinaries(self, word):
        first_part = word[0:4][::-1]
        second_part = word[4:8][::-1]
        print(first_part, second_part)
        result = []
        carry = 0
        for i in range(4):
            first_bit = first_part[i]
            second_bit = second_part[i]
            if first_bit + second_bit + carry == 3:
                result.append(1)
            elif first_bit + second_bit + carry == 2:
                result.append(0)
                carry = 1
            elif first_bit + second_bit + carry == 1:
                result.append(1)
                carry = 0
            else:
                result.append(0)
        result.append(carry)
        return result[::-1]

    def diagonalView(self):
        for i in range(16):
            self.write(i, self.__normal_view[i])

    def normalView(self):
        self.__normal_view.clear()
        for i in range(16):
            self.__normal_view.append(self.read(i))

    def greater(self, word_1, word_2):
        g = False
        l = False
        for i in range(16):
            g = g or ((not bool(word_2[i])) and bool(word_1[i]) and (not l))
            l = l or (bool(word_2[i]) and (not bool(word_1[i])) and (not g))
        if g == True and l == False:
            return True
        return False

    def readLine(self, address):
        return self.__memory[address]

    def read(self, address):
        word = []
        for j in range(address, 16):
            word.append(self.__memory[j][address])
        for j in range(0, address):
            word.append(self.__memory[j][address])
        return word

    def write(self, address, _word):
        word = _word.copy()[::-1]
        for j in range(address, 16):
            self.__memory[j][address] = word.pop()
        for j in range(0, address - 1):
            self.__memory[j][address] = word.pop()

    def print(self):
        print("Diagonal view:\n")
        for row in self.__memory:
            print(row)
        self.normalView()
        print("Normal view:\n")
        for row in self.__normal_view:
            print(row)
