from importlib import import_module


def initialise(day: int, skip_test: bool = True):
    """
    Dynamically load and instantiate the `Solution` class for a specific puzzle day.

    Args:
        day (int): The day number (1-25) of the puzzle to initialize.
        skip_test (bool, optional): Whether to skip test input and use puzzle input.
                                  Defaults to True.

    Returns:
        Solution: An instance of the day's `Solution` class, initialized with the
                 specified parameters.

    Note:
        - Expects solution modules to be named `dayXX.py` where `XX` is zero-padded day number
        - Expects each solution module to have a `Solution` class
        - Solution modules should be in the `solutions` package
        - Solution class must accept `day` and `skip_test` parameters in constructor

    Example:
        >>> solution = initialise(1)  # Uses puzzle input
        >>> test_solution = initialise(1, skip_test=False)  # Uses test input
    """
    module_name = f"solutions.day{day:02d}"
    solution_module = import_module(module_name)
    Solution = getattr(solution_module, "Solution")

    return Solution(day=day, skip_test=skip_test)
