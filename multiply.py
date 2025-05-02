def multiply(a, b):
    """
    Performs multiplication of two numbers.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The result of multiplying a and b.
    """
    try:
        result = a * b
        return result
    except TypeError:
        print("Error: Both inputs must be numbers (int or float).")
        return None

# Example usage
if __name__ == "__main__":
    try:
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))
        result = multiply(a, b)
        if result is not None:
            print(f"The result of multiplying {a} and {b} is: {result}")
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")
