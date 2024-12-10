from importlib import import_module


def initialise(day: int):
    """
    Dynamically load and instantiate the `Solution` class for a specific puzzle day.

    Creates a `Solution` instance for the specified day by dynamically importing
    the appropriate module from the solutions package.

    Args:
        day (int): The day number (1-25) of the puzzle to initialize.

    Returns:
        Solution: An instance of the day's `Solution` class, initialized with the day number.

    Note:
        - Expects solution modules to be named `dayXX.py` where `XX` is zero-padded day number
        - Expects each solution module to have a `Solution` class
        - Solution modules should be in the `solutions` package
        - Solution class must accept `day` parameter in constructor

    Example:
        >>> solution = initialise(1)
        # Imports `solutions.day01` and returns `Solution(day=1)`
    """
    # Dynamically import the solution module based on the day
    module_name = f"solutions.day{day:02d}"
    solution_module = import_module(module_name)

    # Get the `Solution` class
    Solution = getattr(solution_module, "Solution")

    # Instantiate and return the `Solution` object
    return Solution(day=day)
