from fractions import Fraction
import numpy as np

class SimplexModel:
    def __init__(self, objective, function, number_variables, number_constraints, lhs_constraints, rhs_constraints, inequality_constraints, variable_constraints):
        #Initialize variables and constraints
        self.number_variables = number_variables
        self.number_constraints = number_constraints
        # Objective function
        self.objective = objective
        self.function = function
        self.optimal = 0
        # Subject to
        self.lhs_constraints = lhs_constraints
        self.rhs_constraints = rhs_constraints
        self.inequality_constraints = inequality_constraints
        self.variable_constraints = variable_constraints


class SimplexService:
    def __init__(self, objective, function, number_variables, number_constraints, lhs_constraints, rhs_constraints, inequality_constraints, variable_constraints):
        # Primary objective self.function
        self.objective = objective
        self.function = function
        self.optimal = 0
        self.variable_labels = []
        self.new_number_variables = 0
        self.curr_variables = []
        # Initialize variable and constraints
        self.number_variables = number_variables
        self.number_constraints = number_constraints
        # Subject to
        self.lhs_constraints = lhs_constraints
        self.rhs_constraints = rhs_constraints
        self.inequality_constraints = inequality_constraints
        self.variable_constraints = variable_constraints

    def standard(self):
        for i in range(self.number_variables):
            self.variable_labels.append(f"x{i + 1}")
        # STEP-1: RHS constraints must be positive
        for row in range(self.number_constraints):
            if self.rhs_constraints[row] < 0:
                self.rhs_constraints[row] *= -1
                if self.inequality_constraints[row] == ">=":
                    self.inequality_constraints[row] = "<="
                elif self.inequality_constraints[row] == "<=":
                    self.inequality_constraints[row] = ">="
                for col in range(self.number_variables):
                    self.lhs_constraints[row][col] *= -1

        for col in range(self.number_variables):
            if self.variable_constraints[col] == "<=":
                self.variable_labels[col] = f"-{self.variable_labels[col]}"
                self.function[col] *= -1
                for row in range(self.number_constraints):
                    self.lhs_constraints[row][col] *= -1
            elif self.variable_constraints[col] == "urs":
                self.variable_labels.insert(col, f"{self.variable_labels[col]}'")
                self.variable_labels[col + 1] = f"{self.variable_labels[col]}'"
                self.function.insert(col, self.function[col])
                self.function[col + 1] *= -1
                for row in range(self.number_constraints):
                    self.lhs_constraints[row].insert(col, self.lhs_constraints[row][col])
                    self.lhs_constraints[row][col + 1] *= -1

        non_slack_variables = len(self.function)
        # STEP-2: All constraints must be equations
        for row in range(self.number_constraints):
            self.lhs_constraints[row].extend([0] * self.number_constraints)

        if self.objective == "max":
            for i in range(non_slack_variables):
                self.function[i] *= -1

        self.function.extend([0] * self.number_constraints)
        self.new_number_variables = len(self.function)

        for row in range(self.number_constraints):
            self.variable_labels.append(f"s{row + 1}")
            if self.inequality_constraints[row] == ">=":
                self.lhs_constraints[row][row + non_slack_variables] = -1
            else:
                self.lhs_constraints[row][row + non_slack_variables] = 1

        return

    # STEP-3: Find Basic Variables
    def basic_variables(self):
        # Transpose the array
        transposed_array = list(map(list, zip(*self.lhs_constraints)))
        # Initialize lists to store the indices of basic variables and their corresponding row indices
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

        # Current Variables
        self.curr_variables = [0] * self.new_number_variables
        for x in basic_variables:
            self.curr_variables[x["col"]] = self.rhs_constraints[x["row"]]

        return

    # STEP-4: Find entering variable
    def enter_variable_index(self):
        min_value = float("inf")
        min_value_index = 0
        for i in range(self.new_number_variables):
            if self.function[i] < min_value:
                min_value = function[i]
                min_value_index = i
            
        if min_value < 0:
            return min_value_index
        else:
            return None 

    # STEP-5: Find leaving variable
    def leave_variable_index(self, enter_index):
        min_value = float("inf")
        min_value_index = 0
        for i in range(self.number_constraints):
            if self.lhs_constraints[i][enter_index] > 0:
                min_ratio = Fraction(self.rhs_constraints[i],self.lhs_constraints[i][enter_index])
                if min_ratio < min_value:
                    min_value = min_ratio
                    min_value_index = i
            
        if min_value != float("inf"):
            return min_value_index
        else:
            return None

    # STEP-6: Perform row operations
    def row_operations(self, enter_index, leave_index):
        normalizer = Fraction(1,self.lhs_constraints[leave_index][enter_index])
        for i in range(self.new_number_variables):
            self.lhs_constraints[leave_index][i] *= normalizer

        self.rhs_constraints[leave_index] *= normalizer

        objective_multiplier = -1 * Fraction(function[enter_index],self.lhs_constraints[leave_index][enter_index])
        for i in range(self.new_number_variables):
            self.function[i] += objective_multiplier * self.lhs_constraints[leave_index][i]

        self.optimal += objective_multiplier * self.rhs_constraints[leave_index]

        constraint_counter = 0
        while constraint_counter < self.number_constraints:
            if constraint_counter != leave_index:
                multiplier = -1 * Fraction(self.lhs_constraints[constraint_counter][enter_index], self.lhs_constraints[leave_index][enter_index])
                for i in range(self.new_number_variables):
                    self.lhs_constraints[constraint_counter][i] += multiplier * self.lhs_constraints[leave_index][i]

                self.rhs_constraints[constraint_counter] += multiplier * self.rhs_constraints[leave_index]
            constraint_counter += 1

        return

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
        
    def solve(self):
        # Solve
        self.standard()

        breaker = 0
        while True:
            if breaker > 10:
                break
            breaker += 1

            self.basic_variables()
            print(self.format1D(self.curr_variables))
            print(self.format1D(self.function))
            print(self.optimal)
            print(self.format2D(self.lhs_constraints))
            print(self.format1D(self.rhs_constraints))
            print("==============================================================")
            enter_index = self.enter_variable_index()
            if enter_index is not None:
                leave_index = self.leave_variable_index(enter_index)
                if leave_index is not None:
                    self.row_operations(enter_index, leave_index)
                else:
                    print("Problem is unbounded!")
                    break
            else:
                # # Check for zero coefficient non-basic variables
                # for i in range(new_number_variables):
                #     if function[i] == 0 and curr_variables[i] == 0:
                #         print("Non-basic Variable coefficient 0!")
                #         enter_index = i
                #         leave_index = leave_variable_index(number_constraints, lhs_constraints, rhs_constraints, enter_index)
                #         function, optimal, lhs_constraints, rhs_constraints = row_operations(new_number_variables, number_constraints, function, optimal, lhs_constraints, rhs_constraints, enter_index, leave_index)
                #         curr_variables = basic_variables(new_number_variables ,lhs_constraints, rhs_constraints)
                #         print(format1D(curr_variables))
                #         print(format1D(function))
                #         print(optimal)
                #         print(format2D(lhs_constraints))
                #         print(format1D(rhs_constraints))
                #         print("==============================================================")
                #         break
                print("Optimal solution")
                break
