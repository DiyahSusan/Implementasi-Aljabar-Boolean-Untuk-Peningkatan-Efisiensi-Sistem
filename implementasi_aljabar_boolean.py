import sympy
from sympy.abc import A, B, C, D
import numpy as np


def simplify_boolean(expression):
    try:
        parsed_expr = sympy.sympify(expression, evaluate=False)
        simplified_expr = sympy.simplify_logic(parsed_expr)
        return simplified_expr
    except Exception as e:
        return f"Error: {e}"

def generate_truth_table(expression):
    try:
        parsed_expr = sympy.sympify(expression, evaluate=False)
        variables = list(parsed_expr.free_symbols)
        rows = [dict(zip(variables, values)) for values in np.ndindex((2,) * len(variables))]

        #tabel kebenaran
        print("\nTruth Table")
        print("-" * 40)
        print(" | ".join([str(var) for var in variables] + ["Output"]))
        print("-" * 40)
        for row in rows:
            result = int(bool(parsed_expr.subs(row)))  
            print(" | ".join([str(int(row.get(var, 0))) for var in variables] + [str(result)]))

        return rows, variables, parsed_expr

    except Exception as e:
        print(f"Error: {e}")

def count_gates(expression):
    expr = sympy.sympify(expression)
    and_count = str(expr).count('&')
    or_count = str(expr).count('|')
    not_count = str(expr).count('~')
    return and_count + or_count + not_count

def calculate_efficiency(original_expr, simplified_expr):
    try:
        # literals
        original_literals = sum(1 for _ in sympy.sympify(original_expr).atoms(sympy.Symbol))
        simplified_literals = sum(1 for _ in sympy.simplify_logic(simplified_expr).atoms(sympy.Symbol))

        # gates
        original_gates = count_gates(original_expr)
        simplified_gates = count_gates(simplified_expr)

        # persentase
        literal_reduction = ((original_literals - simplified_literals) / original_literals) * 100 if original_literals > 0 else 0
        gate_reduction = ((original_gates - simplified_gates) / original_gates) * 100 if original_gates > 0 else 0

        return literal_reduction, gate_reduction, original_literals, simplified_literals, original_gates, simplified_gates
    except Exception as e:
        return f"Error calculating efficiency: {e}", 0, 0, 0, 0, 0

def generate_karnaugh_map_terminal(rows, variables, parsed_expr):
    try:
        if len(variables) not in [2, 3, 4]: #versi yang terbatas untuk maksimal 4 variabel
            print("Karnaugh maps are only supported for 2, 3, or 4 variables.")
            return

        # membuat grid
        if len(variables) == 2:
            grid = np.zeros((2, 2), dtype=int)
            row_labels = ["0", "1"]
            col_labels = ["0", "1"]
        elif len(variables) == 3:
            grid = np.zeros((2, 4), dtype=int)
            row_labels = ["0", "1"]
            col_labels = ["00", "01", "11", "10"]
        elif len(variables) == 4:
            grid = np.zeros((4, 4), dtype=int)
            row_labels = ["00", "01", "11", "10"]
            col_labels = ["00", "01", "11", "10"]

        # formatting baris dan kolom
        for row in rows:
            inputs = [int(row[var]) for var in variables]
            result = int(bool(parsed_expr.subs(row)))  

            if len(variables) == 2:
                grid[inputs[0], inputs[1]] = result
            elif len(variables) == 3:
                grid[inputs[0], 2 * inputs[1] + inputs[2]] = result
            elif len(variables) == 4:
                grid[2 * inputs[0] + inputs[1], 2 * inputs[2] + inputs[3]] = result

        # peta karnaugh
        print("\nKarnaugh Map:")
        print("   " + "  ".join(col_labels))
        print("  " + "-" * (len(col_labels) * 4 + 1))
        for i, row_label in enumerate(row_labels):
            row_output = " | ".join(str(grid[i, j]) for j in range(grid.shape[1]))
            print(f"{row_label} | {row_output} |")
            print("  " + "-" * (len(col_labels) * 4 + 1))

    except Exception as e:
        print(f"Error generating Karnaugh Map: {e}")

if __name__ == "__main__":
    print("Boolean Simplification Tool")
    print("Enter 'exit' to quit.")

    while True:
        user_input = input("\nEnter a Boolean expression: ")

        if user_input.lower() == "exit":
            break

        print("\nSimplified Expression:")
        simplified_expr = simplify_boolean(user_input)
        print(simplified_expr)

        

        truth_table_data = generate_truth_table(user_input)
        if truth_table_data:
            rows, variables, parsed_expr = truth_table_data
            generate_karnaugh_map_terminal(rows, variables, parsed_expr)

        # Calculate efficiency
        literal_reduction, gate_reduction, original_literals, simplified_literals, original_gates, simplified_gates = calculate_efficiency(user_input, simplified_expr)
        print(f"\nLiteral Reduction: {literal_reduction:.2f}%")
        print(f"Gate Reduction: {gate_reduction:.2f}%")
        print(f"Original Literal Count: {original_literals}, Simplified Literal Count: {simplified_literals}")
        print(f"Original Gate Count: {original_gates}, Simplified Gate Count: {simplified_gates}")
