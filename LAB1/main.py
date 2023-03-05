class Number:
    number_input = None
    normal = None
    straight = None
    reverse = None
    additional = None
    is_negative_number = None
    need_to_add = None

    def __init__(self, number_input, max_size):
        if "." in number_input:
            self.normal = abs(float(number_input))
            self.float_to_binary()
        else:
            self.is_negative_number = True if "-" in number_input else False
            self.number_input = self.normal = abs(int(number_input))
            self.need_to_add = max_size
            self.decimal_to_binary_straight()
            self.decimal_to_binary_reverse()
            self.decimal_to_binary_additional()

    def decimal_to_binary_straight(self):
        result = []
        while self.number_input > 0:
            remainder_of_division = int(float(self.number_input % 2))
            result.append(remainder_of_division)
            self.number_input = (self.number_input - remainder_of_division) / 2
        self.need_to_add -= len(result)
        if self.is_negative_number:
            while self.need_to_add > 1:
                result.append(0)
                self.need_to_add -= 1
            result.append(1)
        else:
            while self.need_to_add > 1:
                result.append(0)
                self.need_to_add -= 1
            result.append(0)
        result.reverse()
        self.straight = ""
        for number in result:
            self.straight += str(number)

    def decimal_to_binary_reverse(self):
        if self.is_negative_number is False:
            self.reverse = self.straight
            self.additional = self.straight
        else:
            abs_binary = self.straight[1:]
            self.reverse = "1"
            for number in abs_binary:
                if number == "1":
                    self.reverse += "0"
                else:
                    self.reverse += "1"

    def decimal_to_binary_additional(self):
        if self.additional is None:
            result = []
            for number in self.reverse:
                result.append(int(number))
            result.reverse()
            result = add_func(result)
            result.reverse()
            self.additional = ""
            for number in result:
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


def add_func(result):
    plus = True
    counter = 0
    for number in result:
        if plus:
            if number == 0:
                result[counter] += 1
                break
            elif number == 1:
                result[counter] -= 1
                counter += 1
                if len(result) < counter:
                    result[counter] += 1
                    plus = False
        else:
            if number == 2:
                result[counter] -= 2
                counter += 1
                if len(result) < counter:
                    result[counter] += 1
    return result


def comparison(tick_of_bits, bit_size, number, result):
    if tick_of_bits < bit_size:
        return result.zfill(bit_size)
    if number < 0:
        return str(1) + result[1:]
    else:
        return str(0) + result[1:]


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
    return comparison(tick_of_bits, bit_size, number, result)


def add_two_binary_numbers(first_number, second_number, max_size, negative_exist):
    result = ""
    carry = 0
    for i in range(max_size - 1, -1, -1):
        sum = carry
        sum += 1 if first_number[i] == "1" else 0
        sum += 1 if second_number[i] == "1" else 0
        result = ("1" if sum % 2 == 1 else "0") + result
        carry = 0 if sum < 2 else 1
    if carry != 0:
        if negative_exist is False:
            result = "1" + result
    return result.zfill(max_size)


def additional_to_straight(binary, is_negative_number):
    abs_binary = binary[1:]
    if is_negative_number:
        straight = "1"
    else:
        straight = "0"
    for number in abs_binary:
        if number == "1":
            straight += "0"
        else:
            straight += "1"
    abs_binary = [int(number) for number in straight[1:]]
    abs_binary.reverse()
    abs_binary = add_func(abs_binary)
    abs_binary.reverse()
    straight = straight[0]
    for number in abs_binary:
        straight += str(number)
    return straight


def binary_to_decimal(binary):
    decimal = i = 0
    is_negative_number = False if binary[0] == "0" else True
    binary_number = get_binary_int(binary)
    if binary_number == 0:
        return binary_number
    while binary_number != 0:
        dec = binary_number % 10
        decimal = decimal + dec * pow(2, i)
        binary_number = binary_number // 10
        i += 1
    if is_negative_number:
        return "-" + str(decimal)
    else:
        return str(decimal)


def get_binary_int(binary):
    abs_binary = binary[1:]
    binary_number = ""
    found = None
    for number in abs_binary:
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


def binary_product(first, second):
    i = remainder = binary_prod = 0
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
        binary_prod = (binary_prod * 10) + sum[i]
        i -= 1
    return binary_prod


def identify_sign(first_number, second_number):
    if first_number[0] == "1" and second_number[0] == "1":
        return "0"
    elif first_number[0] == "1" and second_number[0] == "0":
        return "1"
    elif first_number[0] == "0" and second_number[0] == "1":
        return "1"
    else:
        return "0"


def multiplication_two_binary_numbers(first_number, second_number, max_size):
    multiplication_sign = identify_sign(first_number, second_number)
    binary_multiply = 0
    factor = 1
    first_binary = get_binary_int(first_number)
    second_binary = get_binary_int(second_number)
    while second_binary != 0:
        digit = second_binary % 10
        if digit == 1:
            first_binary = first_binary * factor
            binary_multiply = binary_product(first_binary, binary_multiply)
        else:
            first_binary = first_binary * factor
        second_binary = int(second_binary / 10)
        factor = 10
    binary_multiply = str(binary_multiply)
    binary_multiply = binary_multiply.zfill(max_size - 1)
    binary_multiply = multiplication_sign + str(binary_multiply)
    return binary_multiply


def subtraction(first_number, second_number):
    max_len = max(len(first_number), len(second_number))
    first_number = first_number.zfill(max_len)
    second_number = second_number.zfill(max_len)
    result = ''
    sign_result = 0
    for i in range(max_len - 1, -1, -1):
        num = int(first_number[i]) - int(second_number[i]) - sign_result
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


def division_two_binary_numbers(first_number, second_number, max_size):
    result = carry = ""
    first_number_without_sign = first_number[1:].lstrip("0")
    second_number_without_sign = second_number[1:].lstrip("0")
    for i in range(0, len(first_number_without_sign)):
        carry += first_number_without_sign[i]
        if int(second_number_without_sign) > int(carry):
            result += "0"
        else:
            surplus = subtraction(carry, second_number_without_sign)
            if surplus == 0:
                carry = ""
                result += "1"
            else:
                surplus = str(surplus).lstrip("0")
                result += "1"
                carry = surplus
    result = result.zfill(max_size - 1)
    return identify_sign(first_number, second_number) + result


def identify_exp(first_number, second_number):
    first_number_search = first_number.find("1", 0, first_number.find("."))
    second_number_search = second_number.find("1", 0, second_number.find("."))
    if first_number.find("1", 0, first_number.find(".")) == -1:
        first_exp = 0
    else:
        first_exp = first_number.find(".") - first_number_search - 1
    if second_number.find("1", 0, second_number.find(".")) == -1:
        second_exp = 0
    else:
        second_exp = second_number.find(".") - second_number_search - 1
    return first_exp, second_exp


def add_two_float_numbers(first_number, second_number):
    first_exp, second_exp = identify_exp(first_number, second_number)
    if first_exp >= second_exp:
        diff_exp = first_exp - second_exp
        second_float = "0" * diff_exp + second_number[:(second_number.find("."))] + \
                       second_number[(second_number.find(".") + 1):(len(second_number) - diff_exp)]
        first_float = first_number[:(first_number.find("."))] + first_number[(first_number.find(".") + 1):]
    else:
        diff_exp = second_exp - first_exp
        first_float = "0" * diff_exp + first_number[:(first_number.find("."))] + \
                      first_number[(first_number.find(".") + 1):(len(first_number) - diff_exp)]
        second_float = second_number[:(second_number.find("."))] + second_number[(second_number.find(".") + 1):]
    sum = add_two_binary_numbers(first_float, second_float, len(first_float), False)
    need_to_add = len(sum) - len(second_float)
    result = sum[:max(first_number.find("."), second_number.find(".")) + need_to_add] + "." + \
             sum[(max(first_exp, second_exp) + 1 + need_to_add):]
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


first_number_temp = input("First Number: ")
second_number_temp = input("Second Number: ")

if "." in first_number_temp and second_number_temp:
    first_number = Number(first_number_temp, None)
    second_number = Number(second_number_temp, None)
    print("Прямой:", first_number.straight, second_number.straight)
    sum = add_two_float_numbers(first_number.straight, second_number.straight)
    sum_float = decimal_to_float(sum)
    sum_decimal = float_to_decimal(sum_float)
    print("Сумма:", sum, "-->", sum_float, "-->", sum_decimal, "-->", round(float(sum_decimal), 1))
else:
    max_size = max_size_temp = max(abs(int(first_number_temp)).bit_length(), abs(int(second_number_temp)).bit_length())
    while max_size % 8 != 0 or max_size <= max_size_temp:
        max_size += 1
    first_number = Number(first_number_temp, max_size)
    second_number = Number(second_number_temp, max_size)
    print("\nПрямой:", first_number.straight, second_number.straight)
    print("Обратный:", first_number.reverse, second_number.reverse)
    print("Дополнительный:", first_number.additional, second_number.additional)
    ready_first = first_number.additional if first_number.is_negative_number else first_number.straight
    ready_second = second_number.additional if second_number.is_negative_number else second_number.straight
    bool = True if first_number.is_negative_number or second_number.is_negative_number else False
    sum = add_two_binary_numbers(ready_first, ready_second, max_size, bool)
    if first_number.is_negative_number and second_number.is_negative_number:
        sum_straight = additional_to_straight(sum, True)
        sum_normal = binary_to_decimal(sum_straight)
        print("\nСумма | Разница:", sum, "-->", sum_straight, "-->", sum_normal)
    elif first_number.normal > second_number.normal and first_number.is_negative_number:
        sum_straight = additional_to_straight(sum, True)
        sum_normal = binary_to_decimal(sum_straight)
        print("\nСумма | Разница:", sum, "-->", sum_straight, "-->", sum_normal)
    elif second_number.normal > first_number.normal and second_number.is_negative_number:
        sum_straight = additional_to_straight(sum, True)
        sum_normal = binary_to_decimal(sum_straight)
        print("\nСумма | Разница:", sum, "-->", sum_straight, "-->", sum_normal)
    else:
        sum_normal = binary_to_decimal(sum)
        print("\nСумма | Разность:", sum, "-->", sum_normal)
    while max_size % 8 != 0 or max_size <= (first_number.normal * second_number.normal).bit_length():
        max_size += 1
    multiplication = multiplication_two_binary_numbers(first_number.straight, second_number.straight, max_size)
    multiplication_normal = binary_to_decimal(multiplication)
    print("Произведение:", multiplication, "-->", multiplication_normal)
    division = division_two_binary_numbers(first_number.straight, second_number.straight, max_size)
    division_normal = binary_to_decimal(division)
    print("Частное:", division, "-->", division_normal)
