from function import *
import pre_calc

def find_main_operator(expr, op):
    """Find operator not in parentheses, right-to-left for +- and **, left-to-right for */"""
    depth = 0
    right_to_left = op in ["+", "-", "**"]
    if right_to_left:
        i = len(expr) - 1
        step = -1
        end = -1
    else:
        i = 0
        step = 1
        end = len(expr)

    while i != end:
        if expr[i] == ")":
            depth += 1
        elif expr[i] == "(":
            depth -= 1
        elif depth == 0:
            if expr[i:i+len(op)] == op:
                return i
        i += step
    return -1



def lim(f, a=None, h=1e-5, tol=None, infinity=False, negative=False):
    """
    Compute the limit of f at x = a (finite) or at infinity.

    Parameters:
        f        : Function object
        a        : point to approach (None for infinity)
        h        : small step for finite limits
        tol      : tolerance for numerical comparison (optional)
        infinity : True to compute limit at +∞
        negative : True to compute limit at -∞
    """
    # Auto-adjust tolerance
    if tol is None:
        tol = h * 10

    # ----- Finite limit -----
    if not infinity and not negative:
        try:
            left = f(x=a - h)
            right = f(x=a + h)
        except ZeroDivisionError:
            return "undefined"

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if abs(left - right) < tol:
                return (left + right) / 2
            else:
                return "does not exist"
        else:
            return "cannot evaluate limit with unknown variables"

    # ----- Limit at +∞ or -∞ -----
    x_val = 1e5 if infinity else -1e5
    prev = f(x=x_val)

    for _ in range(10):  # increase x several times
        x_val *= 10
        try:
            curr = f(x=x_val)
        except ZeroDivisionError:
            return "undefined"

        if isinstance(prev, (int, float)) and isinstance(curr, (int, float)):
            if abs(curr - prev) < tol:
                return curr  # stabilized
        prev = curr

    return "does not stabilize / diverges"
