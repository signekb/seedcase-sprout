"""Mimicking the functional programming tools from R and the R package purrr."""

from typing import Callable


def _map(x: list, fn: Callable) -> list:
    """Use a function on each item in a list.

    This is a simpler, more user-friendly version of the built-in `map()`
    function. This function takes a list and a function, applies the function
    to each item in the list, and returns a new list with the results.
    This is mostly a wrapper around the built-in `map()` function.

    Inspired from the functionals from the R package purrr.

    Args:
        x: A list object.
        fn: A function to use on each item in the list `x`.

    Returns:
        A list with the results of applying `fn` to each item in `x`.
        The length of the list is the same as `x`.

    Examples:
        ```{python}
        from seedcase_sprout.core.internals import _map
        def square(x):
            return x * x
        _map([1, 2, 3], square)
        ```
    """
    return list(map(fn, x))
