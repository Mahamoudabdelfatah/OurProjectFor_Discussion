

import sys # To exit cleanly
import add
import subtract
import multiply
import divide
import factorial # Import the new factorial module

# Define constants directly in main.py
ALLOWED_OPERATORS = ['+', '-', '*', '/', '!']
UNARY_OPERATORS = ['!'] # Operators that take only one number
EXIT_COMMAND = 'quit'

# Create a dictionary to map operator symbols to the functions
OPERATIONS_MAP = {
    '+': add.add,
    '-': subtract.subtract,
    '*': multiply.multiply,
    '/': divide.divide,
    '!': factorial.factorial, # Map '!' to the factorial function
}

def run_calculator():
    """Runs the main calculator loop."""
    print("--- Simple College Calculator ---")
    print(f"Allowed operators: {', '.join(ALLOWED_OPERATORS)}")
    print(f"Type '{EXIT_COMMAND}' to exit.")
    print("-" * 30)

    while True:
        # 1. Get Operator
        operator = input("Enter operator (+, -, *, /, !) or 'quit': ").strip()

        if operator.lower() == EXIT_COMMAND:
            print("Exiting calculator. Goodbye!")
            sys.exit()

        if operator not in ALLOWED_OPERATORS:
            print(f"Error: Invalid operator. Please use one of: {', '.join(ALLOWED_OPERATORS)}")
            print("-" * 30)
            continue # Skip the rest of this loop iteration

        # 2. Get Numbers based on operator type
        num1_str = input("Enter first number or 'quit': ").strip()
        if num1_str.lower() == EXIT_COMMAND:
             print("Exiting calculator. Goodbye!")
             sys.exit()

        if operator not in UNARY_OPERATORS: # If it's a binary operator
            num2_str = input("Enter second number or 'quit': ").strip()
            if num2_str.lower() == EXIT_COMMAND:
                print("Exiting calculator. Goodbye!")
                sys.exit()

        # 3. Validate and Convert Numbers
        try:
            num1 = float(num1_str)
            if operator not in UNARY_OPERATORS:
                 num2 = float(num2_str)
        except ValueError:
            print("Error: Invalid number input.")
            print("-" * 30)
            continue # Skip the rest of this loop iteration

        # 4. Perform Calculation
        try:
            operation_func = OPERATIONS_MAP[operator]

            if operator in UNARY_OPERATORS:
                # For factorial, check if it's an integer and non-negative before calling
                if num1 < 0 or not num1.is_integer():
                    # factorial.py will also raise ValueError, but checking here gives a specific message
                     raise ValueError("Factorial is only defined for non-negative integers.")
                # Factorial function in factorial.py expects an integer
                result = operation_func(int(num1))
            else:
                # For binary operations
                result = operation_func(num1, num2)

            # 5. Display Result
            print(f"Result: {result}")
            print("-" * 30)

        except ValueError as e:
            # Catch errors like division by zero (from divide.py) or invalid factorial input
            print(f"Error: {e}")
            print("-" * 30)
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            print("-" * 30)


# This ensures run_calculator() is called when you execute main.py
if __name__ == "__main__":
    run_calculator()