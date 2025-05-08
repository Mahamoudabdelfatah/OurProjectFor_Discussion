# Simple Modular Python Calculator

This project is a basic command-line calculator designed to demonstrate modular programming principles by distributing its functionality across **6 separate Python files**. This structure was specifically chosen to fulfill a requirement for showcasing distinct code components.

## Features

The calculator supports the following operations:

*   **Addition** (`+`)
*   **Subtraction** (`-`)
*   **Multiplication** (`*`)
*   **Division** (`/`) - Includes a check for division by zero.
*   **Factorial** (`!`) - Calculates the factorial of a non-negative integer.

It also includes a simple way to exit the application by typing `'quit'`.

## File Structure

The application is divided into the following 6 files, each with a specific role:

1.  `main.py`
    *   This is the **main entry point** of the application.
    *   It handles the user interaction loop (getting input).
    *   It performs basic **input validation** (checking if input is a number or a valid operator).
    *   It uses a dictionary (`OPERATIONS_MAP`) to **map operator symbols** (`+`, `-`, etc.) to the correct function from the respective operation files.
    *   It **calls the appropriate function** based on the user's operator choice.
    *   It **catches and displays errors** raised by the operation functions (like division by zero).
    *   It displays the final result.

2.  `add.py`
    *   Contains a single function, `add(a, b)`, which performs **addition**.

3.  `subtract.py`
    *   Contains a single function, `subtract(a, b)`, which performs **subtraction**.

4.  `multiply.py`
    *   Contains a single function, `multiply(a, b)`, which performs **multiplication**.

5.  `divide.py`
    *   Contains a single function, `divide(a, b)`, which performs **division**.
    *   Includes a check to raise a `ValueError` if attempting to divide by zero.

6.  `factorial.py`
    *   Contains a single function, `factorial(n)`, which calculates the **factorial** of a non-negative integer `n`.
    *   Raises a `ValueError` for invalid input (negative numbers or non-integers).
    *   Leverages Python's built-in `math.factorial` for efficiency.

## How it Works (Modular Design)

The core idea is **separation of concerns**:

*   Each mathematical operation is isolated in its own file, making the code for each operation simple and easy to understand.
*   `main.py` doesn't need to contain the logic for addition or division itself. It only needs to know *which* file and *which* function to call based on the operator symbol provided by the user.
*   The `OPERATIONS_MAP` in `main.py` is key to this. It acts as a look-up table, connecting the user's input (`'+'`) to the code that performs the action (`add.add`).
*   This modularity makes the code easier to manage, test (you can test each operation function independently), and extend (adding a new operation would involve creating a new file and updating the map in `main.py`).

## How to Run

1.  Save all 6 Python files (`main.py`, `add.py`, `subtract.py`, `multiply.py`, `divide.py`, `factorial.py`) into the **same directory** on your computer.
2.  Open your terminal or command prompt.
3.  Navigate to the directory where you saved the files using the `cd` command (e.g., `cd /path/to/your/calculator`).
4.  Run the main application file using the Python interpreter:
    ```bash
    python main.py
    ```
5.  Follow the on-screen prompts to enter numbers and operators.
6.  Type `quit` at any prompt to exit the calculator.

This structure effectively demonstrates how a program's logic can be broken down into smaller, manageable, and reusable modules, which is a fundamental concept in software development.
