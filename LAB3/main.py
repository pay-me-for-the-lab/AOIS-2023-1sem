import re
from copy import deepcopy
from prettytable import PrettyTable


#              LAB 2


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


def negation_replacement(table, formula, index):
    formula = formula.replace("!x1", str(abs(table[index][0] - 1)))
    formula = formula.replace("!x2", str(abs(table[index][1] - 1)))
    formula = formula.replace("!x3", str(abs(table[index][2] - 1)))
    return formula


def positive_replacement(table, formula, index):
    formula = formula.replace('x1', str(table[index][0]))
    formula = formula.replace('x2', str(table[index][1]))
    formula = formula.replace('x3', str(table[index][2]))
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


def show_pdnf_and_pcnf(table):
    sknf_string = sdnf_string = ''
    for index in range(0, 8):
        if table[index][3] == 0:
            sknf_string += '( x1 + ' if table[index][0] == 0 else '( !x1 + '
            sknf_string += 'x2 + ' if table[index][1] == 0 else '!x2 + '
            sknf_string += 'x3 )*' if table[index][2] == 0 else '!x3 )*'
        else:
            sdnf_string += '( x1 * ' if table[index][0] == 1 else '( !x1 * '
            sdnf_string += 'x2 * ' if table[index][1] == 1 else '!x2 * '
            sdnf_string += 'x3 )+' if table[index][2] == 1 else '!x3 )+'
    sknf_string = sknf_string[:-1]
    sdnf_string = sdnf_string[:-1]
    sdnf_without_space = sdnf_string.replace(' ', '')
    sknf_without_space = sknf_string.replace(' ', '')
    print('Perfect Disjunctive Normal Form (СДНФ):',
          'Formula does not exist' if sdnf_without_space == '' else sdnf_without_space)
    print('Perfect Conjunctive Normal Form (СКНФ):',
          'Formula does not exist' if sknf_without_space == '' else sknf_without_space)
    return sdnf_string, sknf_string


#              №1 METHOD


def replace_arguments_pdnf(partial_formula, current_implicat_index, full_formula):
    values_of_arguments = {full_formula[current_implicat_index][j]: '1'
                           for j in range(len(full_formula[current_implicat_index]))}
    for j in range(len(full_formula[current_implicat_index])):
        var_name = full_formula[current_implicat_index][j][1:] if partial_formula[current_implicat_index][j][0] != 'x' \
            else '!' + full_formula[current_implicat_index][j]
        values_of_arguments[var_name] = '0'
        partial_formula[current_implicat_index][j] = '1'
    return partial_formula, values_of_arguments


def replace_arguments_pcnf(partial_formula, current_implicat_index, full_formula):
    values_of_arguments = {full_formula[current_implicat_index][j]: '0'
                           for j in range(len(full_formula[current_implicat_index]))}
    for j in range(len(full_formula[current_implicat_index])):
        var_name = full_formula[current_implicat_index][j][1:] if partial_formula[current_implicat_index][j][0] != 'x' \
            else '!' + full_formula[current_implicat_index][j]
        values_of_arguments[var_name] = '1'
        partial_formula[current_implicat_index][j] = '0'
    return partial_formula, values_of_arguments


def remove_implications(formula, form):
    formula_after_removed_implicats = []
    if len(formula) == 1 or len(formula[0]) == 1:
        return formula
    for i in range(len(formula)):
        temp_formula = deepcopy(formula)
        if form == 'pdnf':
            temp_formula, values_of_arguments = replace_arguments_pdnf(temp_formula, i, formula)
        else:
            temp_formula, values_of_arguments = replace_arguments_pcnf(temp_formula, i, formula)
        for j in range(len(temp_formula)):
            for k in range(len(temp_formula[j])):
                if temp_formula[j][k] in values_of_arguments:
                    temp_formula[j][k] = values_of_arguments[temp_formula[j][k]]
        if check_for_cut_back_arguments(temp_formula, form):
            formula_after_removed_implicats.append(formula[i])
    return formula_after_removed_implicats


def connect_implicants(formula):
    form_of_formula = 'pdnf' if ')+(' in formula or ' * ' in formula \
        else 'pcnf' if ')*(' in formula or ' + ' in formula else ''
    for_delete = ['(', ')', '+', '*']
    formula_without_extra_characters = [[]]
    formula = [i * (not (i == ')+(' or i == ')*(')) or ' ' for i in formula.split() if i not in for_delete]
    index_of_space = 0
    for i in formula:
        if i == ' ':
            formula_without_extra_characters.append([])
            index_of_space += 1
        else:
            formula_without_extra_characters[index_of_space].append(i)
    return combine_implicants(formula_without_extra_characters, form_of_formula)


def check_for_extra_implicants_pdnf(expression_terms):
    temp_expression = ''
    expression_terms_copy = deepcopy(expression_terms)
    for term in expression_terms:
        if str(term).isdigit():
            continue
        if term[0] != '!' and '!' + term in expression_terms_copy:
            expression_terms_copy.remove(term)
            expression_terms_copy.remove('!' + term)
            temp_expression = '1'
    for term in expression_terms_copy:
        temp_expression = logical_or(term, temp_expression)
    if temp_expression == '1':
        return True
    return False


def check_for_extra_implicants_pcnf(cut_back_formula):
    return any(i[0] != '!' and '!' + i in cut_back_formula for i in cut_back_formula)


def check_for_cut_back_arguments(formula, form):
    formula_after_open_staples = [logical_and(j[0], *j[1:]) if form == 'pdnf'
                                  else logical_or(j[0], *j[1:]) for j in formula if not ''.join(j).isdigit()]
    return [] if (form == 'pdnf' and check_for_extra_implicants_pdnf(formula_after_open_staples)) or \
                 (form != 'pdnf' and check_for_extra_implicants_pcnf(formula_after_open_staples)) \
        else True


def logical_and(arg1, arg2):
    if arg1 == arg2:
        return arg1
    elif arg1.isdigit() and arg2.isdigit():
        return str(int(arg1) and int(arg2))
    elif arg1[0] == 'x' or arg1[0] == '!':
        return arg1 if arg2 == '1' else '0'
    else:
        return arg2 if arg1 == '1' else '0'


def calculate_formula(formula):
    if not formula:
        return 'Formula does not exist'
    formula_after_glue, base_formula, form_of_formula = connect_implicants(formula)
    formula_after_glue_temp = formula_after_glue
    while True:
        size_of_temp_formula = len(formula_after_glue_temp)
        formula_after_glue_temp, base_formula, form_of_formula = combine_implicants(formula_after_glue_temp,
                                                                                    form_of_formula)
        if len(formula_after_glue_temp[0]) == 1:
            return remove_duplicate_literals([j for i in formula_after_glue_temp for j in i])
        if size_of_temp_formula == len(formula_after_glue_temp):
            break
        size_of_implicat = len(formula_after_glue_temp[0])
        formula_after_glue_temp = [i for i in formula_after_glue_temp if len(i) == size_of_implicat]
    return remove_implications(formula_after_glue, form_of_formula)


def remove_duplicate_literals(formula):
    return [[i] for i in set(formula) - {'!' + x for x in set(formula)}]


def check_implicant_size(implicants):
    return all(len(implicant) == len(implicants[0]) for implicant in implicants) if implicants else False


def combine_implicants(implicants, form):
    implicants_after_glue, difference, append_later, used_implicants = [], [], [], []
    if not check_implicant_size(implicants) or len(implicants) == 1:
        return implicants, implicants, form
    for i in range(0, len(implicants) - 1):
        implicant_size = len(implicants_after_glue)
        for k in range(i + 1, len(implicants)):
            for j in range(0, len(implicants[i])):
                if implicants[i][j] != implicants[k][j]:
                    difference.append((implicants[i][j], implicants[k][j]))
            if len(difference) == 1 and difference[0][0][-1] == difference[0][1][-1]:
                implicants_after_glue.append(
                    glue_common_literals(implicants[i], implicants[k]))
                used_implicants.append(implicants[k])
            difference.clear()
        if len(implicants_after_glue) == implicant_size and implicants[i] not in used_implicants:
            append_later.append(implicants[i])
    if len(implicants_after_glue) == 0:
        return implicants, implicants, form
    else:
        implicants_after_glue = append_later + implicants_after_glue + \
                                ([implicants[-1]] if implicants[-1] not in used_implicants else [])
    return implicants_after_glue, implicants, form


def glue_common_literals(imp1, imp2):
    return [imp1[i] for i in range(len(imp1)) if imp1[i] == imp2[i]]


def logical_or(arg1, arg2):
    if arg1.isdigit() and arg2.isdigit():
        return str(int(arg1) or int(arg2))
    if '1' in [arg1, arg2]:
        return '1'
    if arg1[0] in 'x!' and arg2 == '1':
        return '1'
    return arg1 if arg1 == arg2 else arg2


def generate_pcnf_pdnf(formula, form):
    output_formula = []
    if isinstance(formula, str):
        print(formula)
        return '0'
    if len(formula[0]) == 1:
        output_formula.append('(')
    for i in formula:
        if len(i) == 1:
            if form == 'pdnf':
                implicat = f'{" * ".join(i)}+'
            else:
                implicat = f'{" + ".join(i)}*'
        else:
            if form == 'pdnf':
                implicat = f'({" * ".join(i)})+'
            else:
                implicat = f'({" + ".join(i)})*'
        implicat = implicat.replace(' ', '')
        output_formula.append(implicat)
    if len(formula[0]) == 1:
        output_formula[-1] = output_formula[-1][:-1] + ')'
        print(''.join(output_formula))
    else:
        print(''.join(output_formula)[:-1])


#              №2 METHOD


def tabular_calculation_method(glued_formula, default_formula, form):
    while True:
        size = len(glued_formula)
        glued_formula, temp_base_formula, form = combine_implicants(
            glued_formula, form)
        if len(glued_formula[0]) == 1:
            glued_formula = remove_duplicate_literals(list(set(j for i in glued_formula for j in i)))
        if size == len(glued_formula):
            break
        if not glued_formula:
            return '0'
        size_of_implicat = len(glued_formula[0])
        if any(len(i) != size_of_implicat for i in glued_formula):
            return generate_implicant_table(glued_formula, default_formula)
    return generate_implicant_table(glued_formula, default_formula)


def generate_implicant_table(glued_formula, default_formula):
    table = PrettyTable()
    table.field_names = ['  ', *default_formula]
    table_data = [[all([k in j for k in i]) * '+' for j in default_formula] for i in glued_formula]
    for row in zip(glued_formula, table_data):
        table.add_row([row[0], *row[1]])
    print(table)
    index_of_delete_row = delete_row(table_data)
    while index_of_delete_row is not None:
        del glued_formula[index_of_delete_row]
        del table_data[index_of_delete_row]
        index_of_delete_row = delete_row(table_data)
    return glued_formula


def delete_row(table):
    for i in table:
        new_table = table[:]
        new_table.remove(i)
        amount_implicats = {}
        for j in new_table:
            for k in range(len(j)):
                if k not in amount_implicats and j[k] == '+':
                    amount_implicats[k] = 1
                elif k in amount_implicats and j[k] == '+':
                    amount_implicats[k] += 1
        if len(amount_implicats) == len(table[0]):
            return table.index(i)
    return None


#              №3 METHOD


def list_to_dict(lst):
    return [{f"x{i + 1}": x for i, x in enumerate(item[:-1])} | {"f": item[-1], "i": 0} for item in lst]


def minimize_formula_table_method(formula_string, num_input_values, truth_table):
    logical_formula, base_formula, form_of_formula = connect_implicants(formula_string)
    temp_table = generate_truth_table(num_input_values, truth_table)
    if len(logical_formula) == 1:
        return logical_formula
    if form_of_formula == 'pdnf':
        minimized_formula = combine_implicants(generate_formula(minimize_logical_function_by_table_method(
            temp_table, form_of_formula), 'pdnf'), form_of_formula)[0]
    else:
        minimized_formula = combine_implicants(generate_formula(minimize_logical_function_by_table_method(
            temp_table, form_of_formula), 'pcnf'), form_of_formula)[0]
    if len(minimized_formula) == 1 and not minimized_formula[0]:
        return '0'
    return minimized_formula


def generate_truth_table(input_variables, truth_table_data):
    num_input_variables = len(input_variables)
    num_rows = num_input_variables // 2
    num_columns = num_input_variables - num_rows
    table = PrettyTable()
    row_names = generate_binary_combinations(num_rows, input_variables[:num_rows])
    column_names = generate_binary_combinations(num_columns, input_variables[-num_columns:])
    table.field_names = [f'{"".join(input_variables[:num_rows])}/{"".join(input_variables[-num_columns:])}',
                         *[''.join(map(str, i)) for i in transform_dict_values_to_list(column_names)]]
    table_data_list = transform_table_data_to_list(truth_table_data)
    temp_table, index_for_insert_cell = [], -1
    for row in row_names:
        temp_table.append([])
        index_for_insert_cell += 1
        output = []
        for column in column_names:
            temp_row = row | column
            for data_row in table_data_list:
                if temp_row in data_row:
                    temp_table[index_for_insert_cell].append((temp_row, data_row[1]))
                    output.append(data_row[1])
                    break
        table.add_row([''.join(map(str, list(row.values()))), *output])
    print(table)
    return temp_table


def transform_table_data_to_list(table):
    return [[{j: k for j, k in i.items() if j != 'i' and j != 'f'}, list(i.values())[-2]] for i in table]


def transform_dict_values_to_list(table):
    return [list(i.values()) for i in table]


def generate_binary_combinations(args, val):
    string = [{i: 0 for i in val}]
    for i in range(1, 2 ** args):
        for j in range(args - 1, -1, -1):
            string_in_table = string[i - 1].copy()
            index = list(string_in_table.keys())[j]
            string_in_table[index] = 0
            if string_in_table not in string:
                string.append(string_in_table)
                break
            string_in_table[index] = 1
            if string_in_table not in string:
                string.append(string_in_table)
                break
    return string


def minimize_logical_function_by_table_method(table, form):
    if check_all_elements_in_group(table, int(form == 'pdnf')):
        return table
    array_of_groups = [[] for _ in range(3)]
    for i, row in enumerate(table):
        for j, val in enumerate(row):
            group_idx = check_four_group(table, i, j, int(form == 'pdnf'))
            add_group_to_array(group_idx, array_of_groups, val)
            if all(check_group_adjacency(table, i, j, int(form == 'pdnf'))):
                array_of_groups[-1].append((val,))
            group_result = get_adjacent_cells_matching_value(table, i, j, int(form == 'pdnf'))
            add_group_to_array(group_result, array_of_groups, val)
    return array_of_groups


def add_group_to_array(new_group, groups_array, element):
    all_elements = [k for i in groups_array for j in i for k in j]
    if len(new_group) == 0:
        return
    if element not in all_elements or len(new_group[0]) == 4:
        for i in new_group:
            if (i not in all_elements and i not in groups_array[-1]) or len(new_group) == 1:
                if isinstance(new_group[0][0], tuple):
                    groups_array[-1].append(i)
                else:
                    groups_array[-1].append((element, i))


def check_group_adjacency(table, current_row, current_column, form):
    top = bottom = left = right = False
    if table[current_row][current_column][1] == form:
        if current_column != len(table[current_row]) - 1:
            if table[current_row][current_column + 1][1] != form:
                right = True
        elif table[current_row][0][1] != form:
            right = True
        if current_column != 0:
            if table[current_row][current_column - 1][1] != form:
                left = True
        elif table[current_row][len(table[current_row]) - 1][1] != form:
            left = True
        if current_row != 0:
            if table[current_row - 1][current_column][1] != form:
                top = True
        else:
            top = True
        if current_row != len(table) - 1:
            if table[current_row + 1][current_column][1] != form:
                bottom = True
        else:
            bottom = True
    return top, bottom, left, right


def get_adjacent_cells_matching_value(table, current_row, current_column, form):
    answer = []
    if table[current_row][current_column][1] == form:
        if current_column != len(table[current_row]) - 1:
            if table[current_row][current_column + 1][1] == form:
                answer.append(table[current_row][current_column + 1])
        elif table[current_row][0][1] == form:
            answer.append(table[current_row][0])
        if current_column != 0:
            if table[current_row][current_column - 1][1] == form:
                answer.append(table[current_row][current_column - 1])
        elif table[current_row][len(table[current_row]) - 1][1] == form:
            answer.append(table[current_row][len(table[current_row]) - 1])
        if current_row != 0:
            if table[current_row - 1][current_column][1] == form:
                answer.append(table[current_row - 1][current_column])
        if current_row != len(table) - 1:
            if table[current_row + 1][current_column][1] == form:
                answer.append(table[current_row + 1][current_column])
    return answer


def check_four_group(table, current_row, current_column, form):
    elements_in_group = []
    if table[current_row][current_column][1] == form:
        if current_column == 0:
            group_of_elements = []
            for i in range(current_column, len(table[current_row])):
                if table[current_row][i][1] == form:
                    group_of_elements.append(table[current_row][i])
                else:
                    break
            if table[current_row][0][1] == form:
                for i in range(0, current_column):
                    if table[current_row][i][1] == form:
                        group_of_elements.append(table[current_row][i])
                    else:
                        break
            if len(group_of_elements) == 4:
                elements_in_group.append(tuple(group_of_elements))
        elements_in_group += find_four_square_elements(table, current_row, current_column, form)
    return elements_in_group


def find_four_square_elements(table, current_row, current_column, form):
    elements_in_group = []
    if table[current_row][current_column][1] == form:
        if current_row == 0:
            if current_column != len(table[current_row]) - 1:
                if table[current_row][current_column + 1][1] == form \
                        and table[current_row + 1][current_column][1] == form \
                        and table[current_row + 1][current_column + 1][1] == form:
                    elements_in_group.append((table[current_row][current_column],
                                              table[current_row][current_column + 1],
                                              table[current_row + 1][current_column],
                                              table[current_row + 1][current_column + 1]))
            else:
                if table[current_row][0][1] == form \
                        and table[current_row + 1][current_column][1] == form \
                        and table[current_row + 1][0][1] == form:
                    elements_in_group.append((table[current_row][current_column],
                                              table[current_row + 1][current_column],
                                              table[current_row][0],
                                              table[current_row + 1][0]))
    return elements_in_group


def generate_implicants(data, cur_elem):
    for index in range(len(cur_elem)):
        for i in cur_elem[index][0].items():
            if index == 0:
                data[i[0]] = (True, i[1])
            elif data[i[0]][0]:
                data[i[0]] = (bool(True * (not data[i[0]][1] != i[1])), i[1])
    return data


def check_all_elements_in_group(table, form):
    return all(j[1] == form for i in table for j in i)


def generate_formula(args, form):
    create_implicat = []
    data_about_argument = dict()
    for i in args:
        for j in i:
            data_about_argument = generate_implicants(data_about_argument, j)
            if form == 'pdnf':
                create_implicat.append(['!' * (x[1][1] == 0) + x[0] for x in data_about_argument.items() if x[1][0]])
            elif form == 'pcnf':
                create_implicat.append(['!' * (x[1][1] == 1) + x[0] for x in data_about_argument.items() if x[1][0]])
    temp_create_implicat = deepcopy(create_implicat)
    for i in temp_create_implicat:
        if create_implicat.count(i) > 1:
            create_implicat.remove(i)
    return create_implicat


def main():
    formula = [
        '(!((x1+x3)*(!(x2*x3))))',
        '(!(x1*x2)+!(x2*x3))',
        '((x3*x2)+(x2+!x1))',
    ]

    for item in formula:
        print('Formula:', item)
        table = generate_table()
        table = result(table, item)
        pdnf_string, pcnf_string = show_pdnf_and_pcnf(table)
        print('\n[Calculation method]')
        generate_pcnf_pdnf(calculate_formula(pdnf_string), 'pdnf')
        generate_pcnf_pdnf(calculate_formula(pcnf_string), 'pcnf')
        print('\n[Kwaina-McCluskey method]')
        generate_pcnf_pdnf(tabular_calculation_method(*connect_implicants(pdnf_string)), 'pdnf')
        generate_pcnf_pdnf(tabular_calculation_method(*connect_implicants(pcnf_string)), 'pcnf')
        print('\n[Veitch Carnot method]')
        table = list_to_dict(table)
        generate_pcnf_pdnf(minimize_formula_table_method(pdnf_string, ['x1', 'x2', 'x3'], table), 'pdnf')
        generate_pcnf_pdnf(minimize_formula_table_method(pcnf_string, ['x1', 'x2', 'x3'], table), 'pcnf')
        print('\n\n')


main()
