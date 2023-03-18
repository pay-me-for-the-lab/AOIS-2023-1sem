import re
from prettytable import PrettyTable


def generate_table():
    table = [[0 for x in range(4)] for y in range(8)]
    control = 0
    for index in range(8):
        if index < 4:
            table[index][0] = 0
        else:
            table[index][0] = 1
        if control == 4:
            control = 0
        if control < 2:
            table[index][1] = 0
        else:
            table[index][1] = 1
        if index % 2 == 0:
            table[index][2] = 0
        else:
            table[index][2] = 1
        control = control + 1
    return table


def show_table(table):
    design = PrettyTable()
    design.field_names = ["a", "b", "c", "Result"]
    for index in range(8):
        design.add_row([table[index][0], table[index][1], table[index][2], True if table[index][3] == 1 else False])
    print(design)


def negation_replacement(table, formula, index):
    formula = formula.replace("!a", str(abs(table[index][0] - 1)))
    formula = formula.replace("!b", str(abs(table[index][1] - 1)))
    formula = formula.replace("!c", str(abs(table[index][2] - 1)))
    return formula


def positive_replacement(table, formula, index):
    formula = formula.replace('a', str(table[index][0]))
    formula = formula.replace('b', str(table[index][1]))
    formula = formula.replace('c', str(table[index][2]))
    return formula


def sign_replacement(formula):
    formula = formula.replace("+", "or")
    formula = formula.replace("*", "and")
    return formula


def result(table, formula):
    temp_formula = formula
    for index in range(8):
        temp_formula = negation_replacement(table, temp_formula, index)
        temp_formula = positive_replacement(table, temp_formula, index)
        temp_formula = sign_replacement(temp_formula)
        table[index][3] = formula_result(temp_formula)
        temp_formula = formula
    return table


def formula_calculate(formula):
    formula = formula[1:len(formula) - 1]
    if "or" in formula:
        if formula[0] == "0" and formula[3] == "0":
            return "0"
        else:
            return "1"
    elif "and" in formula:
        if formula[0] == "1" and formula[4] == "1":
            return "1"
        else:
            return "0"


def formula_result(formula):
    while re.search(r'\([01]+[or|and]+[01]+\)', formula):
        original_formula = re.search(r'\([01]+[or|and]+[01]+\)', formula).group()
        calculated_formula = formula_calculate(re.search(r'\([01]+[or|and]+[01]+\)', formula).group())
        formula = formula.replace(original_formula, calculated_formula)
    if "(!1)" in formula or "(!0)" in formula:
        formula = formula.replace("(!1)", "0")
        formula = formula.replace("(!0)", "1")
    if "!1" in formula or "!0" in formula:
        formula = formula.replace("!1", "0")
        formula = formula.replace("!0", "1")
    if "or" in formula or "and" in formula:
        formula = formula_result(formula)
    return int(formula)


def show_sknf_and_sdnf(table):
    sknf_string = sdnf_string = ""
    for index in range(0, 8):
        if table[index][3] == 0:
            sknf_string += "(a+" if table[index][0] == 0 else "(!a+"
            sknf_string += "b+" if table[index][1] == 0 else "!b+"
            sknf_string += "c)*" if table[index][2] == 0 else "!c)*"
        else:
            sdnf_string += "(a*" if table[index][0] == 1 else "(!a*"
            sdnf_string += "b*" if table[index][1] == 1 else "!b*"
            sdnf_string += "c)+" if table[index][2] == 1 else "!c)+"
    sknf_string = sknf_string[:-1]
    sdnf_string = sdnf_string[:-1]
    print("Perfect Disjunctive Normal Form (СДНФ):", sdnf_string)
    print("Perfect Conjunctive Normal Form (СКНФ):", sknf_string)


def binary_for_sknf_and_sdnf(table):
    sknf_string = sdnf_string = ""
    for index in range(0, 8):
        if table[index][3] == 0:
            sknf_string += str(table[index][0]) + str(table[index][1]) + str(table[index][2]) + " "
        else:
            sdnf_string += str(table[index][0]) + str(table[index][1]) + str(table[index][2]) + " "
    print("\nBinary (СДНФ):", sdnf_string)
    print("Binary (СКНФ):", sknf_string)
    return sknf_string, sdnf_string


def binary_to_decimal(number):
    decimal_number = 0
    for i in range(1, len(number) + 1):
        decimal_number += int(number[-i]) * pow(2, i - 1)
    return decimal_number


def decimal_for_sknf_and_sdnf(sdnf, sknf):
    decimal_sdnf, decimal_sknf = [], []
    while sdnf != "":
        decimal_sdnf.append(sdnf[:sdnf.find(" ")])
        sdnf = sdnf[sdnf.find(" ") + 1:]
    while sknf != "":
        decimal_sknf.append(sknf[:sknf.find(" ")])
        sknf = sknf[sknf.find(" ") + 1:]
    for value in range(len(decimal_sdnf)):
        decimal_sdnf[value] = str(binary_to_decimal(decimal_sdnf[value]))
    for value in range(len(decimal_sknf)):
        decimal_sknf[value] = str(binary_to_decimal(decimal_sknf[value]))
    print("\nDecimal (СДНФ):", " ".join(decimal_sdnf))
    print("Decimal (СКНФ):", " ".join(decimal_sknf))


def main():
    # formula = "(!((!a+c)*(!(b*!c))))"
    formula = input("Enter the formula: ")
    table = generate_table()
    table = result(table, formula)
    show_table(table)
    show_sknf_and_sdnf(table)
    binary_sknf, binary_sdnf = binary_for_sknf_and_sdnf(table)
    decimal_for_sknf_and_sdnf(binary_sdnf, binary_sknf)


main()
