from collections import defaultdict
from fractions import Fraction
import numpy as np

# Standardize the model
def standard(objective, function, optimal, number_variables, number_constraints, lhs_constraints, rhs_constraints, inequality_constraints, variable_constraints):
    variable_labels = []
    for i in range(number_variables):
        variable_labels.append(f"x{i + 1}")
    # STEP-1: RHS constraints must be positive
    for row in range(number_constraints):
        if rhs_constraints[row] < 0:
            rhs_constraints[row] *= -1
            if inequality_constraints[row] == ">=":
                inequality_constraints[row] = "<="
            elif inequality_constraints[row] == "<=":
                inequality_constraints[row] = ">="
            for col in range(number_variables):
                lhs_constraints[row][col] *= -1

    for col in range(number_variables):
        if variable_constraints[col] == "<=":
            variable_labels[col] = f"-{variable_labels[col]}"
            function[col] *= -1
            for row in range(number_constraints):
                lhs_constraints[row][col] *= -1
        elif variable_constraints[col] == "urs":
            variable_labels.insert(col, f"{variable_labels[col]}'")
            variable_labels[col + 1] = f"{variable_labels[col]}'"
            function.insert(col, function[col])
            function[col + 1] *= -1
            for row in range(number_constraints):
                lhs_constraints[row].insert(col, lhs_constraints[row][col])
                lhs_constraints[row][col + 1] *= -1

    non_slack_variables = len(function)
    # STEP-2: All constraints must be equations
    for row in range(number_constraints):
        lhs_constraints[row].extend([0] * number_constraints)

    if objective == "max":
        for i in range(non_slack_variables):
            function[i] *= -1

    function.extend([0] * number_constraints)
    new_number_variables = len(function)

    for row in range(number_constraints):
        variable_labels.append(f"s{row + 1}")
        if inequality_constraints[row] == ">=":
            lhs_constraints[row][row + non_slack_variables] = -1
        else:
            lhs_constraints[row][row + non_slack_variables] = 1

    return new_number_variables, function, optimal, lhs_constraints, rhs_constraints, variable_labels

def basic_variables(new_number_variables, lhs_constraints, rhs_constraints):
    # STEP-3: Find Basic Variables
    # Transpose the array
    transposed_array = list(map(list, zip(*lhs_constraints)))
    # Initialize lists to store the indices of basic variables and their corresponding row indices
    basic_vars = []
    basic_var_rows = []
    basic_variables = []
    def exist(target, arr):
        for i in range(len(arr)):
            if arr[i]["row"] == target:
                return i
        
        return None
    # Loop through each row of the transposed array
    for i, row in enumerate(transposed_array):
        # Count the number of non-zero values in the row
        num_nonzero = sum(val != 0 for val in row)
        # If there is only one non-zero value, add the index to the list of basic variables
        # and append the row index to the list of corresponding row indices
        if num_nonzero == 1:
            row_index = row.index(next(val for val in row if val != 0))
            exist_index = exist(row_index, basic_variables)
            if exist_index is not None:
                basic_variables[exist_index] = {"row": row_index, "col": i}
            else:
                basic_variables.append({"row": row_index, "col": i})
            
            basic_vars.append(i)
            basic_var_rows.append(row.index(next(val for val in row if val != 0)))

    # Current Variables
    curr_variables = [0] * new_number_variables
    for x in basic_variables:
        curr_variables[x["col"]] = rhs_constraints[x["row"]]

    return curr_variables

# STEP-4: Find entering variable
def enter_variable_index(new_number_variables, function):
    min_value = float("inf")
    min_value_index = 0
    for i in range(new_number_variables):
        if function[i] < min_value:
            min_value = function[i]
            min_value_index = i
        
    if min_value < 0:
        return min_value_index
    else:
        return None

# STEP-5: Find leaving variable
def leave_variable_index(number_constraints, lhs_constraints, rhs_constraints, enter_index):
    min_value = float("inf")
    min_value_index = 0
    for i in range(number_constraints):
        if lhs_constraints[i][enter_index] > 0:
            min_ratio = Fraction(rhs_constraints[i],lhs_constraints[i][enter_index])
            if min_ratio < min_value:
                min_value = min_ratio
                min_value_index = i
        
    if min_value != float("inf"):
        return min_value_index
    else:
        return None

# STEP-6: Perform row operations
def row_operations(new_number_variables, number_constraints, function, optimal, lhs_constraints, rhs_constraints, enter_index, leave_index):
    normalizer = Fraction(1,lhs_constraints[leave_index][enter_index])
    for i in range(new_number_variables):
        lhs_constraints[leave_index][i] *= normalizer

    rhs_constraints[leave_index] *= normalizer

    objective_multiplier = -1 * Fraction(function[enter_index],lhs_constraints[leave_index][enter_index])
    for i in range(new_number_variables):
        function[i] += objective_multiplier * lhs_constraints[leave_index][i]

    optimal += objective_multiplier * rhs_constraints[leave_index]

    constraint_counter = 0
    while constraint_counter < number_constraints:
        if constraint_counter != leave_index:
            multiplier = -1 * Fraction(lhs_constraints[constraint_counter][enter_index], lhs_constraints[leave_index][enter_index])
            for i in range(new_number_variables):
                lhs_constraints[constraint_counter][i] += multiplier * lhs_constraints[leave_index][i]

            rhs_constraints[constraint_counter] += multiplier * rhs_constraints[leave_index]
        constraint_counter += 1

    return function, optimal, lhs_constraints, rhs_constraints

def format1D(arr):
    result = []
    for i in arr:
        result.append(str(i))

    return np.array(result)

def format2D(arr):
    result = []
    for i in arr:
        row = []
        for j in i:
            row.append(str(j))

        result.append(np.array(row))

    return np.array(result)

def solve():
    # Input Q1
    objective = "max"
    function = [2, -1, 1, 0]
    optimal = 0

    number_variables = 4
    number_constraints = 3

    lhs_constraints = [[1, -1, 3, 1], [2, 1, 0, 0], [1, -1, -1, 0]]
    rhs_constraints = [4, 10, 7]
    inequality_constraints = ["=", "<=", "<="]
    variable_constraints = [">=", ">=", ">=", ">="]

    # # Input Q2
    # objective = "max"
    # function = [1, 4, 2]
    # optimal = 0

    # number_variables = 3
    # number_constraints = 2

    # lhs_constraints = [[4, 1, 2], [1, -1, -2]]
    # rhs_constraints = [5, -10]
    # inequality_constraints = ["<=", ">="]
    # variable_constraints = ["urs", ">=", ">="]

    # # Input Q3
    # objective = "max"
    # function = [5, 1, 4, 4]
    # optimal = 0

    # number_variables = 4
    # number_constraints = 3

    # lhs_constraints = [[1,-2,4,3],[-4,6,5,-4],[2,-3,3,8]]
    # rhs_constraints = [20, 40, 50]
    # inequality_constraints = ["<=", "<=", "<="]
    # variable_constraints = [">=", ">=", ">=", ">="]

    # # Input Q4
    # objective = "max"
    # function = [5,3,1]
    # optimal = 0

    # number_variables = 3
    # number_constraints = 2

    # lhs_constraints = [[1,1,3],[5,3,6]]
    # rhs_constraints = [6,15]
    # inequality_constraints = ["<=", "<="]
    # variable_constraints = [">=", ">=", ">="]

    # Solve
    new_number_variables, function, optimal, lhs_constraints, rhs_constraints, variable_labels = standard(objective, function, optimal, number_variables, number_constraints, lhs_constraints, rhs_constraints, inequality_constraints, variable_constraints)
    print(variable_labels)
    # print(function)
    # print(lhs_constraints)
    # print(rhs_constraints)

    breaker = 0
    while True:
        if breaker > 10:
            break
        breaker += 1

        curr_variables = basic_variables(new_number_variables ,lhs_constraints, rhs_constraints)
        print(format1D(curr_variables))
        print(format1D(function))
        print(optimal)
        print(format2D(lhs_constraints))
        print(format1D(rhs_constraints))
        print("==============================================================")
        enter_index = enter_variable_index(new_number_variables, function)
        if enter_index is not None:
            leave_index = leave_variable_index(number_constraints, lhs_constraints, rhs_constraints, enter_index)
            if leave_index is not None:
                function, optimal, lhs_constraints, rhs_constraints = row_operations(new_number_variables, number_constraints, function, optimal, lhs_constraints, rhs_constraints, enter_index, leave_index)
            else:
                print("Problem is unbounded!")
                break
        else:
            # Check for zero coefficient non-basic variables
            for i in range(new_number_variables):
                if function[i] == 0 and curr_variables[i] == 0:
                    print("Non-basic Variable coefficient 0!")
                    enter_index = i
                    leave_index = leave_variable_index(number_constraints, lhs_constraints, rhs_constraints, enter_index)
                    function, optimal, lhs_constraints, rhs_constraints = row_operations(new_number_variables, number_constraints, function, optimal, lhs_constraints, rhs_constraints, enter_index, leave_index)
                    curr_variables = basic_variables(new_number_variables ,lhs_constraints, rhs_constraints)
                    print(format1D(curr_variables))
                    print(format1D(function))
                    print(optimal)
                    print(format2D(lhs_constraints))
                    print(format1D(rhs_constraints))
                    print("==============================================================")
                    break
            print("Optimal solution")
            break

solve()