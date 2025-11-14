import errno


class Variable:
    def __init__(self, name):
        self.name = name


def insert_implied_multiplication(expr):
    """Insert * where multiplication is implied, e.g., 2x, 2(3), (x+1)(x+2)"""
    new_expr = ""
    for i in range(len(expr) - 1):
        new_expr += expr[i]
        # If current char is digit or ')' and next char is '(' or letter, insert '*'
        if (expr[i].isdigit() or expr[i] == ")"):
            if expr[i + 1] == "(" or expr[i + 1].isalpha():
                new_expr += "*"
        # If current char is a letter and next char is '(', also insert '*'
        if expr[i].isalpha() and expr[i + 1] == "(":
            new_expr += "*"
    new_expr += expr[-1]
    return new_expr

class Function:
    def __init__(self, expression):
        expr = expression.replace(" ", "")
        expr = insert_implied_multiplication(expr)
        self.expression = expr

    def __call__(self, **values):
        result, _ = self._evaluate(self.expression, values)
        return result

    def _evaluate(self, expr, values):
        expr = expr.strip()

        # Remove outer parentheses
        while expr.startswith("(") and expr.endswith(")"):
            depth = 0
            for i, c in enumerate(expr):
                if c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                if depth == 0 and i != len(expr) - 1:
                    break
            else:
                expr = expr[1:-1]
                continue
            break

        # Base case: number
        try:
            return float(expr), True
        except ValueError:
            pass

        # Variable
        if expr.isalpha():
            if expr in values:
                return float(values[expr]), True
            else:
                return expr, False  # unknown variable

        # ----- PEMDAS: ** first (right-associative) -----
        index = self._find_main_operator(expr, "**")
        if index != -1:
            left_val, left_num = self._evaluate(expr[:index], values)
            right_val, right_num = self._evaluate(expr[index + 2:], values)
            if left_num and right_num:
                return left_val ** right_val, True
            else:
                return f"({left_val}**{right_val})", False

        # ----- Then * / (left-associative) -----
        for op in ["*", "/"]:
            index = self._find_main_operator(expr, op)
            if index != -1:
                left_val, left_num = self._evaluate(expr[:index], values)
                right_val, right_num = self._evaluate(expr[index + 1:], values)
                if left_num and right_num:
                    if op == "*":
                        return left_val * right_val, True
                    else:
                        if right_val == 0:
                            return "undefined", False
                        return left_val / right_val, True
                else:
                    return f"({left_val}{op}{right_val})", False

        # ----- Then + - (right-associative) -----
        for op in ["+", "-"]:
            index = self._find_main_operator(expr, op)
            if index != -1:
                left_val, left_num = self._evaluate(expr[:index], values)
                right_val, right_num = self._evaluate(expr[index + 1:], values)
                if left_num and right_num:
                    if op == "+":
                        return left_val + right_val, True
                    else:
                        return left_val - right_val, True
                else:
                    return f"({left_val}{op}{right_val})", False

        # Cannot evaluate
        return expr, False

    def _find_main_operator(self, expr, op):
        """Find operator not inside parentheses"""
        depth = 0
        # Right-to-left for + - **, left-to-right for * /
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
                # Check multi-char operator
                if expr[i:i+len(op)] == op:
                    return i
            i += step
        return -1
