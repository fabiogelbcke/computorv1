import sys

import webbrowser

def degree(coef):
    degree = 0
    for deg, value in coef.items():
        degree = int(deg) if int(deg) > degree else degree
    return degree

def print_reduced(coef, degree):
    eqstr = ""
    for i in range(0, degree + 1):
        deg = str(i)
        if deg != "0":
            if deg in coef:
                value = coef[deg]
            else:
                value = 0
            if value < 0:
                value = value * -1
                eqstr += (" - " + str(value))
            else:
                eqstr += (" + " + str(value))
            if deg == "1":
                eqstr += (" * X")
            else:
                eqstr += (" * X^" + deg)
        else:
            value = 0 if not "0" in coef else coef["0"]
            eqstr += (str(value))
    return eqstr

def root(n):
    root = n/2
    sum = n/4
    absv = lambda n : -1 * n if n < 0 else n
    while (absv(root * root - n) > 0.000001):
        if root * root > n:
            root -= sum
        else:
            root += sum
        sum = sum / 2
    return root

def solve_zero(coef):
    if coef["0"] != 0:
        print("There is no possible solution")
    else:
        print("The solution is any number in the realm of all complex numbers");

def solve_linear(coef):
    print "The solution is:"
    print str((-1 * coef["0"]) / (coef["1"]))

def solve_quadratic(coef):
    a = coef["2"]
    b = 0 if not "1" in coef else coef["1"]
    c = 0 if not "0" in coef else coef["0"]
    det = b * b - 4 * a * c
    if det == 0:
        print("The discriminant is 0, which means there only one solution:")
        print(-1 * b / ( 2 * a))
    if det > 0:
        print("The discriminant is greater than zero, which means there are 2 real solutions:")
        print("{0:.6f}".format(((-1 * b) + root(det)) / (2 * a)))
        print("{0:.6f}".format(((-1 * b) - root(det)) / (2 * a)))
    else:
        print("The discriminant is less than zero, therefore there are 2 complex solutions:")
        if b != 0:
            print("{0:.6f}".format((-1 * b) / (2 * a)) + " + i * " + ("{0:.6f}".format(root(-1 * det) / (2 * a))))
            print("{0:.6f}".format((-1 * b) / (2 * a)) + " - i * " + ("{0:.6f}".format(root(-1 * det) / (2 * a))))
        else:
            print("i * " + ("{0:.6f}".format(root(-1 * det) / (2 * a))))
            print("i * -" + ("{0:.6f}".format(root(-1 * det) / (2 * a))))


def handle_args(args, redeq):
    if "graph" in args:
        input = redeq.replace("+", " plus ")
        webbrowser.open('https://www.wolframalpha.com/input/?i=' + input )
    if "blue" in args:
        sys.stdout.write("\x1b[34m")
    elif "yellow" in args:
        sys.stdout.write("\x1b[31m")
    elif "blue" in args:
        sys.stdout.write("\x1b[34m")
    elif "green" in args:
        sys.stdout.write("\x1b[32m")
    elif "red" in args:
        sys.stdout.write("\x1b[31m")

def main():
    table = {0:"0"}
    coef = {}
    sign = 1
    after_equal = 1
    nbr = 0
    last_obj = 1
    if len(sys.argv) < 2:
        print "ComputorV1 takes at least one argument: the equation"
        return
    table = sys.argv[1].split()
    while "*" in table:
        table.remove("*")
    for item in table:
        if item[0] != "=" and item[0] != "X" and item[0] != "+" and (item[0] != "-" or len(item) > 1):
           nbr = float(item)
           last_obj = 0
        elif item[0] == "X":
            if len(item) == 1:
                item = "X^1"
            if item[2:] in coef.keys():
                coef[item[2:]] += nbr * after_equal * sign
            else:
                coef[item[2:]] = nbr * after_equal * sign
            coef[item[2:]] += last_obj * after_equal * sign
            nbr = 0
            last_obj = 0
        elif item[0] == "+":
            if "0" in coef.keys():
                coef["0"] += nbr * after_equal * sign
            else:
                coef["0"] = nbr * after_equal * sign
            sign = 1
            nbr = 0
            last_obj = 1
        elif item[0] == "-":
            if "0" in coef.keys():
                coef["0"] += nbr * after_equal * sign
            else:
                coef["0"] = nbr * after_equal * sign
            sign = -1
            nbr = 0
            last_obj = 1
        elif item[0] == "=":
            if "0" in coef.keys():
                coef["0"] += nbr * after_equal * sign
            else:
                coef["0"] = nbr * after_equal * sign
            nbr = 0
            last_obj = 1
            after_equal = -1
            sign = 1
    if "0" in coef.keys():
        coef["0"] += nbr * after_equal * sign
    else:
        coef["0"] = nbr * after_equal * sign
    deg = degree(coef)
    redeq = print_reduced(coef, deg)
    if len(sys.argv) > 2:
        handle_args(sys.argv, redeq)
    print "Reduced form: " + redeq + " = 0"
    print ("Polynomial degree: " + str(deg))
    if deg > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return
    if deg == 2:
        solve_quadratic(coef)
    elif deg == 1:
        solve_linear(coef)
    elif deg == 0:
        solve_zero(coef)
                    
main()
sys.stdout.write("\x1b[0m")
