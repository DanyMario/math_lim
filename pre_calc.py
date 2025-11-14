import function

def log(x, b=10, step=1e-5):
    if x <= 0 or b <= 0 or b == 1:
        return "undefined"

    y = 0
    power = 1
    while power * b <= x:
        power *= b
        y += 1

    if abs(power * b - x) < 1e-12:
        return y + 1
    elif abs(power - x) < 1e-12:
        return y

    y_approx = 0
    while b ** y_approx < x:
        y_approx += step

    return y_approx


def ln(x, step=1e-5):
    y = 0
    power = 1
    while power < x:
        power =  e() ** y
        y += step
    return y
