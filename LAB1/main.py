class Number:
    numberInput = None
    normal = None
    straight = None
    reverse = None
    additional = None
    negative_number = None
    need_to_add = None

    def __init__(self, numberInput, maxSize):
        if "." in numberInput:
            self.normal = abs(float(numberInput))
            self.float_to_binary()
        else:
            if "-" in numberInput:
                self.negative_number = True
            else:
                self.negative_number = False
            self.numberInput = self.normal = abs(int(numberInput))
            self.need_to_add = maxSize
            self.decimal_to_binary_straight()
            self.decimal_to_binary_reverse()
            self.decimal_to_binary_additional()

    def decimal_to_binary_straight(self):
        temp = []
        while self.numberInput > 0:
            remainder_of_division = int(float(self.numberInput % 2))
            temp.append(remainder_of_division)
            self.numberInput = (self.numberInput - remainder_of_division) / 2
        self.need_to_add -= len(temp)
        if self.negative_number:
            while self.need_to_add > 1:
                temp.append(0)
                self.need_to_add -= 1
            temp.append(1)
        else:
            while self.need_to_add > 1:
                temp.append(0)
                self.need_to_add -= 1
            temp.append(0)
        temp.reverse()
        self.straight = ""
        for number in temp:
            self.straight += str(number)

    def decimal_to_binary_reverse(self):
        if self.negative_number is False:
            self.reverse = self.straight
            self.additional = self.straight
        else:
            temp = self.straight[1:]
            self.reverse = "1"
            for number in temp:
                if number == "1":
                    self.reverse += "0"
                else:
                    self.reverse += "1"

    def decimal_to_binary_additional(self):
        if self.additional is None:
            temp = []
            for number in self.reverse:
                temp.append(int(number))
            temp.reverse()
            plus = True
            counter = 0
            for number in temp:
                if plus:
                    if number == 0:
                        temp[counter] += 1
                        break
                    elif number == 1:
                        temp[counter] -= 1
                        counter += 1
                        if len(temp) < counter:
                            temp[counter] += 1
                            plus = False
                else:
                    if number == 2:
                        temp[counter] -= 2
                        counter += 1
                        if len(temp) < counter:
                            temp[counter] += 1
            temp.reverse()
            self.additional = ""
            for number in temp:
                self.additional += str(number)

    def float_to_binary(self):
        control = 0
        mantissa_size = 23
        int_num = int(self.normal)
        fraction = self.normal - float(int_num)
        int_result = decimal_to_binary_straight(int_num)
        if int_result.find("1"):
            self.straight = int_result[int_result.find("1"):] + "."
        else:
            self.straight = "0" + "."
        while control <= mantissa_size - len(self.straight):
            fraction *= 2
            if int(fraction) == 0:
                self.straight += "0"
            else:
                fraction -= 1
                self.straight += "1"


def decimal_to_binary_straight(number):
    binary = result = ""
    tick_of_actions = tick_of_bits = 0
    clone_of_num = number
    if abs(number) < 100:
        bit_size = 8
    else:
        bit_size = 16
    if number < 0:
        clone_of_num = -number
    if number == 0:
        binary = str(0)
    while clone_of_num >= 1:
        zero_or_unit = str(int(clone_of_num % 2))
        binary = binary + zero_or_unit
        tick_of_bits += 1
        clone_of_num /= 2
        tick_of_actions = tick_of_actions + 1
        result = binary[::-1]
    if tick_of_bits < bit_size:
        result = result.zfill(bit_size)
    if number < 0:
        result = str(1) + result[1:]
    else:
        result = str(0) + result[1:]
    return result


def add_two_binary_numbers(firstNumber, secondNumber, maxSize, negative_exist):
    result = ""
    carry = 0
    for i in range(maxSize - 1, -1, -1):
        sum = carry
        sum += 1 if firstNumber[i] == "1" else 0
        sum += 1 if secondNumber[i] == "1" else 0
        result = ("1" if sum % 2 == 1 else "0") + result
        carry = 0 if sum < 2 else 1
    if carry != 0:
        if negative_exist is False:
            result = "1" + result
    return result.zfill(maxSize)


def additional_to_straight(binary, negative_number):
    temp = binary[1:]
    if negative_number:
        straight = "1"
    else:
        straight = "0"
    for number in temp:
        if number == "1":
            straight += "0"
        else:
            straight += "1"
    temp = [int(number) for number in straight[1:]]
    temp.reverse()
    plus = True
    counter = 0
    for number in temp:
        if plus:
            if number == 0:
                temp[counter] += 1
                break
            elif number == 1:
                temp[counter] -= 1
                counter += 1
                if len(temp) < counter:
                    temp[counter] += 1
                    plus = False
        else:
            if number == 2:
                temp[counter] -= 2
                counter += 1
                if len(temp) < counter:
                    temp[counter] += 1
    temp.reverse()
    straight = straight[0]
    for number in temp:
        straight += str(number)
    return straight


def binary_to_decimal(binary):
    decimal = i = 0
    negative_number = found = None
    binary_number = ""
    if binary[0] == "0":
        negative_number = False
    else:
        negative_number = True
    temp = binary[1:]
    for number in temp:
        if found is None:
            if number == "1":
                binary_number += number
                found = True
                continue
            else:
                continue
        else:
            binary_number += number
    if binary_number:
        binary_number = int(binary_number)
    else:
        decimal = 0
        return decimal
    while binary_number != 0:
        dec = binary_number % 10
        decimal = decimal + dec * pow(2, i)
        binary_number = binary_number // 10
        i += 1
    if negative_number:
        return "-" + str(decimal)
    else:
        return str(decimal)


def get_binary_int(binary):
    temp = binary[1:]
    binary_number = ""
    found = None
    for number in temp:
        if found is None:
            if number == "1":
                binary_number += number
                found = True
                continue
            else:
                continue
        else:
            binary_number += number
    if binary_number:
        binary_number = int(binary_number)
        return binary_number
    else:
        binary_number = 0
        return binary_number


def binaryProduct(first, second):
    i = remainder = binaryProd = 0
    sum = []
    while first != 0 or second != 0:
        sum.insert(i, ((first % 10) + (second % 10) + remainder) % 2)
        remainder = int(((first % 10) + (second % 10) + remainder) / 2)
        first = int(first / 10)
        second = int(second / 10)
        i += 1
    if remainder != 0:
        sum.insert(i, remainder)
        i += 1
    i -= 1
    while i >= 0:
        binaryProd = (binaryProd * 10) + sum[i]
        i -= 1
    return binaryProd


def multiplication_two_binary_numbers(firstNumber, secondNumber, maxSize):
    if firstNumber[0] == "1" and secondNumber[0] == "1":
        multiplication = "0"
    elif firstNumber[0] == "1" and secondNumber[0] == "0":
        multiplication = "1"
    elif firstNumber[0] == "0" and secondNumber[0] == "1":
        multiplication = "1"
    else:
        multiplication = "0"
    binaryMultiply = 0
    factor = 1
    firstBinary = get_binary_int(firstNumber)
    secondBinary = get_binary_int(secondNumber)
    while secondBinary != 0:
        digit = secondBinary % 10
        if digit == 1:
            firstBinary = firstBinary * factor
            binaryMultiply = binaryProduct(firstBinary, binaryMultiply)
        else:
            firstBinary = firstBinary * factor
        secondBinary = int(secondBinary / 10)
        factor = 10
    binaryMultiply = str(binaryMultiply)
    binaryMultiply = binaryMultiply.zfill(maxSize - 1)
    binaryMultiply = multiplication + str(binaryMultiply)
    return binaryMultiply


def subtraction(firstNumber, secondNumber):
    max_len = max(len(firstNumber), len(secondNumber))
    firstNumber = firstNumber.zfill(max_len)
    secondNumber = secondNumber.zfill(max_len)
    result = ''
    sign_result = 0
    for i in range(max_len - 1, -1, -1):
        num = int(firstNumber[i]) - int(secondNumber[i]) - sign_result
        if num % 2 == 1:
            result = '1' + result
        else:
            result = '0' + result
        if num < 0:
            sign_result = 1
        else:
            sign_result = 0
    if sign_result != 0:
        result = '01' + result
    if int(result) == 0:
        result = 0
    return result


def division_two_binary_numbers(firstNumber, secondNumber, maxSize):
    result = carry = ""
    sign_firstNumber = firstNumber[0]
    sign_secondNumber = secondNumber[0]
    firstNumber = firstNumber[1:].lstrip("0")
    secondNumber = secondNumber[1:].lstrip("0")
    for i in range(0, len(firstNumber)):
        carry += firstNumber[i]
        if int(secondNumber) > int(carry):
            result += "0"
        else:
            surplus = subtraction(carry, secondNumber)
            if surplus == 0:
                carry = ""
                result += "1"
            else:
                surplus = str(surplus).lstrip("0")
                result += "1"
                carry = surplus
    result = result.zfill(maxSize - 1)
    if sign_firstNumber == "1" and sign_secondNumber == "1":
        result = "0" + result
    elif sign_firstNumber == "0" and sign_secondNumber == "0":
        result = "0" + result
    else:
        result = "1" + result
    return result


def add_two_float_numbers(fisrtNumber, secondNumber):
    firstNumberSearch = fisrtNumber.find("1", 0, fisrtNumber.find("."))
    secondNumberSearch = secondNumber.find("1", 0, secondNumber.find("."))
    if fisrtNumber.find("1", 0, fisrtNumber.find(".")) == -1:
        firstExp = 0
    else:
        firstExp = fisrtNumber.find(".") - firstNumberSearch - 1
    if secondNumber.find("1", 0, secondNumber.find(".")) == -1:
        secondExp = 0
    else:
        secondExp = secondNumber.find(".") - secondNumberSearch - 1
    if firstExp >= secondExp:
        diff_exp = firstExp - secondExp
        secondFloat = "0" * diff_exp + secondNumber[:(secondNumber.find("."))] + \
                      secondNumber[(secondNumber.find(".") + 1):(len(secondNumber) - diff_exp)]
        firstFloat = fisrtNumber[:(fisrtNumber.find("."))] + fisrtNumber[(fisrtNumber.find(".") + 1):]
    else:
        diff_exp = secondExp - firstExp
        firstFloat = "0" * diff_exp + fisrtNumber[:(fisrtNumber.find("."))] + \
                     fisrtNumber[(fisrtNumber.find(".") + 1):(len(fisrtNumber) - diff_exp)]
        secondFloat = secondNumber[:(secondNumber.find("."))] + secondNumber[(secondNumber.find(".") + 1):]
    sum = add_two_binary_numbers(firstFloat, secondFloat, len(firstFloat), False)
    need_to_add = len(sum) - len(secondFloat)
    result = sum[:max(fisrtNumber.find("."), secondNumber.find(".")) + need_to_add] + "." + \
             sum[(max(firstExp, secondExp) + 1 + need_to_add):]
    return result


def decimal_to_float(number):
    if "1" in number[:number.find(".")]:
        exp_sign = 1
    else:
        exp_sign = -1
    if number.find("1", 0, number.find(".")) == -1:
        exp_bytes = decimal_to_binary_straight(127 + ((number.find("1") - number.find(".")) * exp_sign))[-8:]
    else:
        exp_bytes = decimal_to_binary_straight(127 + ((number.find(".") - number.find("1") - 1) * exp_sign))[-8:]
    result = "0" + " " + exp_bytes + " " + number[number.find("1") + 1:number.find(".")] + number[number.find(".") + 1:]
    return result


def float_to_decimal(number):
    number = number[0] + number[2:10] + number[11:]
    decimal_mantissa = 0.0
    for i in range(9, len(number)):
        decimal_mantissa += int(number[i]) * pow(2, -(i - 8))
    exp = int(binary_to_decimal("0" + number[1:9])) - 127
    result = str((1 + decimal_mantissa) * pow(2, exp))
    return result


firstNumberTemp = input("First Number: ")
secondNumberTemp = input("Second Number: ")

if "." in firstNumberTemp and secondNumberTemp:
    firstNumber = Number(firstNumberTemp, None)
    secondNumber = Number(secondNumberTemp, None)
    print("Прямой:", firstNumber.straight, secondNumber.straight)
    sum = add_two_float_numbers(firstNumber.straight, secondNumber.straight)
    sum_float = decimal_to_float(sum)
    sum_decimal = float_to_decimal(sum_float)
    print("Сумма:", sum, "-->", sum_float, "-->", sum_decimal, "-->", round(float(sum_decimal), 1))
else:
    maxSize = maxSizeTemp = max(abs(int(firstNumberTemp)).bit_length(), abs(int(secondNumberTemp)).bit_length())
    while maxSize % 8 != 0 or maxSize <= maxSizeTemp:
        maxSize += 1
    firstNumber = Number(firstNumberTemp, maxSize)
    secondNumber = Number(secondNumberTemp, maxSize)
    print("\nПрямой:", firstNumber.straight, secondNumber.straight)
    print("Обратный:", firstNumber.reverse, secondNumber.reverse)
    print("Дополнительный:", firstNumber.additional, secondNumber.additional)
    readyFirst = firstNumber.additional if firstNumber.negative_number else firstNumber.straight
    readySecond = secondNumber.additional if secondNumber.negative_number else secondNumber.straight
    bool = True if firstNumber.negative_number or secondNumber.negative_number else False
    sum = add_two_binary_numbers(readyFirst, readySecond, maxSize, bool)
    if firstNumber.negative_number and secondNumber.negative_number:
        sum_straight = additional_to_straight(sum, True)
        sum_normal = binary_to_decimal(sum_straight)
        print("\nСумма | Разница:", sum, "-->", sum_straight, "-->", sum_normal)
    elif firstNumber.normal > secondNumber.normal and firstNumber.negative_number:
        sum_straight = additional_to_straight(sum, True)
        sum_normal = binary_to_decimal(sum_straight)
        print("\nСумма | Разница:", sum, "-->", sum_straight, "-->", sum_normal)
    elif secondNumber.normal > firstNumber.normal and secondNumber.negative_number:
        sum_straight = additional_to_straight(sum, True)
        sum_normal = binary_to_decimal(sum_straight)
        print("\nСумма | Разница:", sum, "-->", sum_straight, "-->", sum_normal)
    else:
        sum_normal = binary_to_decimal(sum)
        print("\nСумма | Разность:", sum, "-->", sum_normal)
    while maxSize % 8 != 0 or maxSize <= (firstNumber.normal * secondNumber.normal).bit_length():
        maxSize += 1
    multiplication = multiplication_two_binary_numbers(firstNumber.straight, secondNumber.straight, maxSize)
    multiplication_normal = binary_to_decimal(multiplication)
    print("Произведение:", multiplication, "-->", multiplication_normal)
    division = division_two_binary_numbers(firstNumber.straight, secondNumber.straight, maxSize)
    division_normal = binary_to_decimal(division)
    print("Частное:", division, "-->", division_normal)
