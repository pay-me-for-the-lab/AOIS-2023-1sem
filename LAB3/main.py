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


def answer(table, formula):
    temp_formula = formula
    for index in range(8):
        temp_formula = negation_replacement(table, temp_formula, index)
        temp_formula = positive_replacement(table, temp_formula, index)
        temp_formula = sign_replacement(temp_formula)
        table[index][3] = formula_answer(temp_formula)
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


def formula_answer(formula):
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
        formula = formula_answer(formula)
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
    glued_formula, default_formula, form = connect_implicants(formula)
    glued_formula_temp = glued_formula
    while True:
        size_of_temp_formula = len(glued_formula_temp)
        glued_formula_temp, default_formula, form = combine_implicants(glued_formula_temp,
                                                                       form)
        if len(glued_formula_temp[0]) == 1:
            return remove_duplicate_literals([j for i in glued_formula_temp for j in i])
        if size_of_temp_formula == len(glued_formula_temp):
            break
        size_of_implicat = len(glued_formula_temp[0])
        glued_formula_temp = [i for i in glued_formula_temp if len(i) == size_of_implicat]
    return remove_implications(glued_formula, form)


def remove_duplicate_literals(formula):
    return [[i] for i in set(formula) - {'!' + x for x in set(formula)}]


def remove_extra_characters(formula):
    for_delete = ['(', ')', '+', '*']
    answer = [[]]
    formula = [i * (not (i == ')+(' or i == ')*(')) or ' ' for i in formula.split() if i not in for_delete]
    space_i = 0
    for i in formula:
        if i == ' ':
            answer.append([])
            space_i += 1
        else:
            answer[space_i].append(i)
    return answer


def has_extra_implicants(expression_terms):
    expression_terms_copy = deepcopy(expression_terms)
    for term in expression_terms:
        if str(term).isdigit():
            continue
        if term[0] != '!' and '!' + term in expression_terms_copy:
            expression_terms_copy.remove(term)
            expression_terms_copy.remove('!' + term)
            return True
    return False


def replace_arguments_pdnf(partial_formula, current_implicat_index, formula):
    argument_values = generate_argument_values_dict_pdnf(formula, current_implicat_index)
    for j in range(len(formula[current_implicat_index])):
        argument_values, partial_formula = update_argument_values_pdnf(argument_values, partial_formula,
                                                                       formula, current_implicat_index, j)
    return partial_formula, argument_values


def generate_argument_values_dict_pcnf(formula, current_implicat_index):
    return {formula[current_implicat_index][j]: '0' for j in range(len(formula[current_implicat_index]))}


def update_argument_values_pcnf(argument_values, partial_formula, formula, current_implicat_index, j):
    if partial_formula[current_implicat_index][j][0] != 'x':
        var_name = formula[current_implicat_index][j][1:]
    else:
        var_name = '!' + formula[current_implicat_index][j]
    argument_values[var_name] = '1'
    partial_formula[current_implicat_index][j] = '0'
    return argument_values, partial_formula


def check_implicant_size(implicants):
    return all(len(implicant) == len(implicants[0]) for implicant in implicants) if implicants else False


def get_difference(implicant1, implicant2):
    answer = []
    for i in range(len(implicant1)):
        if implicant1[i] != implicant2[i]:
            answer.append((implicant1[i], implicant2[i]))
    return answer


def combine_implicants(implicants, form):
    glued_impicants, append_later, used_implicants = [], [], []
    if not check_implicant_size(implicants) or len(implicants) == 1:
        return implicants, implicants, form
    for i in range(0, len(implicants) - 1):
        implicant_size = len(glued_impicants)
        for k in range(i + 1, len(implicants)):
            difference = get_difference(implicants[i], implicants[k])
            if len(difference) == 1 and difference[0][0][-1] == difference[0][1][-1]:
                glued_impicants.append(glue_common_literals(implicants[i], implicants[k]))
                used_implicants.append(implicants[k])
        if len(glued_impicants) == implicant_size and implicants[i] not in used_implicants:
            append_later.append(implicants[i])
    if len(glued_impicants) == 0:
        return implicants, implicants, form
    else:
        glued_impicants = append_later + glued_impicants + (
            [implicants[-1]] if implicants[-1] not in used_implicants else [])
    return glued_impicants, implicants, form


def get_form_of_formula(formula):
    if ')+(' in formula or ' * ' in formula:
        return 'pdnf'
    elif ')*(' in formula or ' + ' in formula:
        return 'pcnf'
    else:
        return ''


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
    answer = []
    if isinstance(formula, str):
        print(formula)
        return '0'
    if len(formula[0]) == 1:
        answer.append('(')
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
        answer.append(implicat)
    if len(formula[0]) == 1:
        answer[-1] = answer[-1][:-1] + ')'
        print(''.join(answer))
    else:
        print(''.join(answer)[:-1])


def replace_arguments_pcnf(partial_formula, current_implicat_index, formula):
    argument_values = generate_argument_values_dict_pcnf(formula, current_implicat_index)
    for j in range(len(formula[current_implicat_index])):
        argument_values, partial_formula = update_argument_values_pcnf(argument_values, partial_formula,
                                                                       formula, current_implicat_index, j)
    return partial_formula, argument_values


def generate_argument_values_dict_pdnf(formula, current_implicat_index):
    return {formula[current_implicat_index][j]: '1' for j in range(len(formula[current_implicat_index]))}


def update_argument_values_pdnf(argument_values, partial_formula, formula, current_implicat_index, j):
    if partial_formula[current_implicat_index][j][0] != 'x':
        var_name = formula[current_implicat_index][j][1:]
    else:
        var_name = '!' + formula[current_implicat_index][j]
    argument_values[var_name] = '0'
    partial_formula[current_implicat_index][j] = '1'
    return argument_values, partial_formula


def remove_implications(formula, form):
    answer = []
    if len(formula) == 1 or len(formula[0]) == 1:
        return formula
    for i in range(len(formula)):
        temp_formula = deepcopy(formula)
        if form == 'pdnf':
            temp_formula, argument_values = replace_arguments_pdnf(temp_formula, i, formula)
        else:
            temp_formula, argument_values = replace_arguments_pcnf(temp_formula, i, formula)
        for j in range(len(temp_formula)):
            for k in range(len(temp_formula[j])):
                if temp_formula[j][k] in argument_values:
                    temp_formula[j][k] = argument_values[temp_formula[j][k]]
        if check_for_cut_back_arguments(temp_formula, form):
            answer.append(formula[i])
    return answer


def connect_implicants(formula):
    form = get_form_of_formula(formula)
    clear_formula = remove_extra_characters(formula)
    return combine_implicants(clear_formula, form)


def check_for_extra_implicants_pdnf(expression_terms):
    temp_expression = ''
    if has_extra_implicants(expression_terms):
        return True
    for term in expression_terms:
        temp_expression = logical_or(term, temp_expression)
    if temp_expression == '1':
        return True
    return False


def check_for_extra_implicants_pcnf(formula):
    return any(i[0] != '!' and '!' + i in formula for i in formula)


def check_for_cut_back_arguments(formula, form):
    formula_without_staples = [logical_and(j[0], *j[1:]) if form == 'pdnf'
                               else logical_or(j[0], *j[1:]) for j in formula if not ''.join(j).isdigit()]
    return [] if (form == 'pdnf' and check_for_extra_implicants_pdnf(formula_without_staples)) or \
                 (form != 'pdnf' and check_for_extra_implicants_pcnf(formula_without_staples)) \
        else True


#              №2 METHOD

def delete_row(table):
    for i in table:
        actual_table = table[:]
        actual_table.remove(i)
        amount_implicats = count_implicats(actual_table)
        if len(amount_implicats) == len(table[0]):
            return find_index(table, i)
    return None


def count_implicats(table):
    answer = {}
    for j in table:
        for k in range(len(j)):
            if k not in answer and j[k] == '+':
                answer[k] = 1
            elif k in answer and j[k] == '+':
                answer[k] += 1
    return answer


def find_index(table, row):
    return table.index(row)


def tabular_calculation_method(glued_formula, default_formula, form):
    while True:
        size = len(glued_formula)
        glued_formula, default_formula_temp, form = combine_implicants(glued_formula, form)
        if len(glued_formula[0]) == 1:
            glued_formula = remove_duplicate_literals(list(set(j for i in glued_formula for j in i)))
        if size == len(glued_formula):
            break
        if not glued_formula:
            return '0'
        implicat_size = len(glued_formula[0])
        if any(len(i) != implicat_size for i in glued_formula):
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


#              №3 METHOD

def is_four_square_group(table, cur_row, cur_col, form):
    if cur_row == 0:
        if cur_col != len(table[cur_row]) - 1:
            if table[cur_row][cur_col + 1][1] == form \
                    and table[cur_row + 1][cur_col][1] == form \
                    and table[cur_row + 1][cur_col + 1][1] == form:
                return True
        else:
            if table[cur_row][0][1] == form \
                    and table[cur_row + 1][cur_col][1] == form \
                    and table[cur_row + 1][0][1] == form:
                return True
    return False


def find_four_square_elements(table, cur_row, cur_col, form):
    answer = []
    if is_four_square_group(table, cur_row, cur_col, form):
        if cur_row == 0:
            if cur_col != len(table[cur_row]) - 1:
                answer.append((table[cur_row][cur_col],
                               table[cur_row][cur_col + 1],
                               table[cur_row + 1][cur_col],
                               table[cur_row + 1][cur_col + 1]))
            else:
                answer.append((table[cur_row][cur_col],
                               table[cur_row + 1][cur_col],
                               table[cur_row][0],
                               table[cur_row + 1][0]))
    return answer


def get_adjacent_cells_matching_value(table, cur_row, cur_col, form):
    answer = []
    answer.extend(get_adjacent_horizontal_cells_matching_value(table, cur_row, cur_col, form))
    answer.extend(get_adjacent_vertical_cells_matching_value(table, cur_row, cur_col, form))
    return answer


def initialize_string(val):
    return [{i: 0 for i in val}]


def get_index_to_update(j, string_in_table):
    index = list(string_in_table.keys())[j]
    string_in_table[index] = 0
    return index, string_in_table


def update_string(string, string_in_table):
    if string_in_table not in string:
        string.append(string_in_table)
        return True
    return False


def generate_binary_combinations(args, val):
    answer = initialize_string(val)
    for i in range(1, 2 ** args):
        for j in range(args - 1, -1, -1):
            string_in_table = answer[i - 1].copy()
            index, string_in_table = get_index_to_update(j, string_in_table)
            if update_string(answer, string_in_table):
                break
            string_in_table[index] = 1
            if update_string(answer, string_in_table):
                break
    return answer


def group_adjacency(table_data, i, j, is_pdnf):
    return all(check_group_adjacency(table_data, i, j, 1 * (is_pdnf == 'pdnf')))


def create_groups(table_data, is_pdnf):
    answer = [[]]
    for i in range(0, len(table_data)):
        for j in range(0, len(table_data[i])):
            add_group_to_array(check_four_group(table_data, i, j, 1 * (is_pdnf == 'pdnf')), answer,
                               table_data[i][j])
    answer.append([])
    for i in range(len(table_data)):
        for j in range(len(table_data[i])):
            if group_adjacency(table_data, i, j, is_pdnf):
                answer[-1].append((table_data[i][j],))
    answer.append([])
    for i in range(len(table_data)):
        for j in range(len(table_data[i])):
            group_answer = get_adjacent_cells_matching_value(
                table_data, i, j, 1 * (is_pdnf == 'pdnf'))
            add_group_to_array(group_answer, answer, table_data[i][j])
    return answer


def minimize_logical_function_by_table_method(table, form):
    if check_all_elements_in_group(table, 1 * (form == 'pdnf')):
        return table
    return create_groups(table, form)


def get_adjacent_vertical_cells_matching_value(table, cur_row, cur_col, form):
    answer = []
    if table[cur_row][cur_col][1] == form:
        if cur_row != 0:
            if table[cur_row - 1][cur_col][1] == form:
                answer.append(table[cur_row - 1][cur_col])
        if cur_row != len(table) - 1:
            if table[cur_row + 1][cur_col][1] == form:
                answer.append(table[cur_row + 1][cur_col])
    return answer


def get_adjacent_horizontal_cells_matching_value(table, current_row, current_column, form):
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
    return answer


def check_four_group(table, cur_row, cur_col, form):
    answer = []
    if table[cur_row][cur_col][1] == form:
        if cur_col == 0:
            group_of_elements = find_group_of_elements(table, cur_row, cur_col, form)
            if len(group_of_elements) == 4:
                answer.append(tuple(group_of_elements))
        answer += find_four_square_elements(table, cur_row, cur_col, form)
    return answer


def generate_row_names(rows_num, input_variables):
    return generate_binary_combinations(rows_num, input_variables[:rows_num])


def generate_column_names(col_num, input_variables):
    return generate_binary_combinations(col_num, input_variables[-col_num:])


def get_output_for_row(row, col_names, table):
    answer = []
    for column in col_names:
        temp_row = row | column
        for data_row in table:
            if temp_row in data_row:
                answer.append(data_row[1])
                break
    return answer


def generate_truth_table(input_variables, truth_table_data):
    num_input_variables = len(input_variables)
    num_rows = num_input_variables // 2
    num_columns = num_input_variables - num_rows
    table = PrettyTable()
    row_names = generate_row_names(num_rows, input_variables)
    column_names = generate_column_names(num_columns, input_variables)
    table.field_names = [f'{"".join(input_variables[:num_rows])}/{"".join(input_variables[-num_columns:])}',
                         *[''.join(map(str, i)) for i in transform_dict_values_to_list(column_names)]]
    table_data_list = transform_table_data_to_list(truth_table_data)
    answer, index_for_insert_cell = [], -1
    for row in row_names:
        answer.append([])
        index_for_insert_cell += 1
        output = get_output_for_row(row, column_names, table_data_list)
        table.add_row([''.join(map(str, list(row.values()))), *output])
        answer[index_for_insert_cell].extend([(row | column, output[i]) for i, column in enumerate(column_names)])
    print(table)
    return answer


def check_conditions(new_group, groups_array, element):
    all_elements = [k for i in groups_array for j in i for k in j]
    if len(new_group) == 0:
        return False
    if element not in all_elements or len(new_group[0]) == 4:
        for i in new_group:
            if (i not in all_elements and i not in groups_array[-1]) or len(new_group) == 1:
                if isinstance(new_group[0][0], tuple):
                    groups_array[-1].append(i)
                else:
                    groups_array[-1].append((element, i))
        return True
    return False


def add_group_to_array(new_group, groups_array, element):
    if check_conditions(new_group, groups_array, element):
        all_elements = [k for i in groups_array for j in i for k in j]
        for i in new_group:
            if (i not in all_elements and i not in groups_array[-1]) or len(new_group) == 1:
                if isinstance(new_group[0][0], tuple):
                    groups_array[-1].append(i)
                else:
                    groups_array[-1].append((element, i))


def find_group_of_elements(table, cur_row, cur_col, form):
    answer = []
    for i in range(cur_col, len(table[cur_row])):
        if table[cur_row][i][1] == form:
            answer.append(table[cur_row][i])
        else:
            break
    if table[cur_row][0][1] == form:
        for i in range(0, cur_col):
            if table[cur_row][i][1] == form:
                answer.append(table[cur_row][i])
            else:
                break
    return answer


def generate_implicants(data, cur_elem):
    for index in range(len(cur_elem)):
        for i in cur_elem[index][0].items():
            if index == 0:
                data[i[0]] = (True, i[1])
            elif data[i[0]][0]:
                data[i[0]] = (bool(True * (not data[i[0]][1] != i[1])), i[1])
    return data


def generate_formula(args, form):
    answer = []
    data_about_argument = dict()
    for i in args:
        for j in i:
            data_about_argument = generate_implicants(data_about_argument, j)
            if form == 'pdnf':
                answer.append(['!' * (x[1][1] == 0) + x[0] for x in data_about_argument.items() if x[1][0]])
            elif form == 'pcnf':
                answer.append(['!' * (x[1][1] == 1) + x[0] for x in data_about_argument.items() if x[1][0]])
    temp_create_implicat = deepcopy(answer)
    for i in temp_create_implicat:
        if answer.count(i) > 1:
            answer.remove(i)
    return answer


def check_group_adjacency(table, current_row, current_column, form):
    up_side = down_side = left_side = right_side = False
    if table[current_row][current_column][1] == form:
        last_column = len(table[current_row]) - 1
        if current_column != 0 and table[current_row][current_column - 1][1] != form or \
                current_column == 0 and table[current_row][last_column][1] != form:
            left_side = True
        if current_column != last_column and table[current_row][current_column + 1][1] != form or \
                current_column == last_column and table[current_row][0][1] != form:
            right_side = True
        if current_row != 0 and table[current_row - 1][current_column][1] != form or \
                current_row == 0:
            up_side = True
        if current_row != len(table) - 1 and table[current_row + 1][current_column][1] != form or \
                current_row == len(table) - 1:
            down_side = True
    return up_side, down_side, left_side, right_side


def transform_table_data_to_list(table):
    return [[{j: k for j, k in i.items() if j != 'i' and j != 'f'}, list(i.values())[-2]] for i in table]


def check_all_elements_in_group(table, form):
    return all(j[1] == form for i in table for j in i)


def transform_dict_values_to_list(table):
    return [list(i.values()) for i in table]


def list_to_dict(lst):
    return [{f"x{i + 1}": x for i, x in enumerate(item[:-1])} | {"f": item[-1], "i": 0} for item in lst]


def minimize_formula_table_method(formula_string, num_input_values, truth_table):
    logical_formula, base_formula, form_of_formula = connect_implicants(formula_string)
    temp_table = generate_truth_table(num_input_values, truth_table)
    if len(logical_formula) == 1:
        return logical_formula
    if form_of_formula == 'pcnf':
        answer = combine_implicants(generate_formula(minimize_logical_function_by_table_method(
            temp_table, form_of_formula), 'pcnf'), form_of_formula)[0]
    else:
        answer = combine_implicants(generate_formula(minimize_logical_function_by_table_method(
            temp_table, form_of_formula), 'pdnf'), form_of_formula)[0]
    if len(answer) == 1 and not answer[0]:
        return '0'
    return answer


def main():
    formula = [
        '((x1+x2)*x3)',
        '(!((x1+x3)*(!(x2*x3))))',
        '(!(x1*x2)+!(x2*x3))',
        '((x3*x2)+(x2+!x1))',
    ]

    for item in formula:
        print('Formula:', item)
        table = generate_table()
        table = answer(table, item)
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
