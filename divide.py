
def divide(a, b):
    """Performs division. Raises ValueError if dividing by zero."""
    if b == 0:
        # Raise a specific error that main.py can catch
        raise ValueError("Cannot divide by zero")
    return a / b