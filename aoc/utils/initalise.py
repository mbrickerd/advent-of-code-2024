from importlib import import_module


def initialise(day: int):
    # Dynamically import the solution module based on the day
    module_name = f"solutions.day{day:02d}"
    solution_module = import_module(module_name)

    # Get the `Solution` class
    Solution = getattr(solution_module, "Solution")

    # Instantiate and return the `Solution` object
    return Solution(day=day)
