import os

expressions = open("day18.input").read().split(os.linesep)


ops = {"+": lambda x, y: x + y, "*": lambda x, y: x * y}

def push(result, stack, op):
    if op:
        stack.append(op(result, stack.pop()))
    else:
        stack.append(result)

def meval(expr, stack, op=None):
    if not expr:
        return stack.pop()

    if expr.startswith("("):
        idx = 1
        parens = 0
        while not (parens == 0 and expr[idx] == ")"):
            if expr[idx] == ")":
                parens -= 1
            if expr[idx] == "(":
                parens += 1
            idx += 1

        result = meval(expr[1:idx], [], [])
        push(result, stack, op)
        return meval(expr[idx + 1:].strip(), stack, op)

    parts = expr.split(" ", 1)
    token = parts[0]
    rest = "" if len(parts) == 1 else parts[1]

    if token.isnumeric():
        push(int(token), stack, op)
        return meval(rest, stack, op)

    if token in ops:
        op = ops[token]
        return meval(rest, stack, op)

    raise IOError(token)


# Part 1 answer
print(sum([meval(expr, []) for expr in expressions]))


def push2(result, stack, opstack):
    if opstack and opstack[-1] == "+":
        opstack.pop()
        stack.append(result + stack.pop())
    else:
        stack.append(result)

def meval2(expr, stack, opstack):
    if not expr:
        while opstack:
            op = ops[opstack.pop()]
            stack.append(op(stack.pop(), stack.pop()))
        return stack.pop()

    if expr.startswith("("):
        idx = 1
        parens = 0
        while not (parens == 0 and expr[idx] == ")"):
            if expr[idx] == ")":
                parens -= 1
            if expr[idx] == "(":
                parens += 1
            idx += 1

        result = meval2(expr[1:idx], [], [])
        push2(result, stack, opstack)
        return meval2(expr[idx + 1:].strip(), stack, opstack)

    parts = expr.split(" ", 1)
    token = parts[0]
    rest = "" if len(parts) == 1 else parts[1]

    if token.isnumeric():
        push2(int(token), stack, opstack)
        return meval2(rest, stack, opstack)

    if token in ops:
        opstack.append(token)
        return meval2(rest, stack, opstack)

    raise IOError(token)


# Part 2 answer
print(sum([meval2(expr, [], []) for expr in expressions]))