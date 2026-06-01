#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_mul(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_div(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mul(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluate(tokens):
    """
    evaluate the given tokens
    highOrder keeps track on if it should do div and mul or add and sub
    """
    tokens = evaluate_high_order(tokens)
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    #first stage of evaluation where it process higher order operation (div and mul)
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def evaluate_high_order(tokens):
    """
    evalaute high order operations(div and mul)
    return new tokens with just lower order (add and sub)
    """
    index = 0
    new_tokens = []
    while index < len(tokens):
        #if we hit the high order operation, we process
        if tokens[index]['type'] in ('DIVIDE', 'MULTIPLY'):
            #get the first number of the operation
            first_num = new_tokens.pop()['number']
            second_num = tokens[index+1]['number']
            #evaluate the number and append on new_tokens list
            #make sure it returns the dictionary form not just a number
            if tokens[index]['type'] == 'DIVIDE':
                new_tokens.append({'type': 'NUMBER', 'number': first_num/second_num})
            else:
                new_tokens.append({'type': 'NUMBER', 'number': first_num*second_num})
            index+=2
        else:
            #if the operation is low level continue
            if tokens[index]['type'] in ('NUMBER', "PLUS", 'MINUS'):
                new_tokens.append(tokens[index])
            else:
                print(f'Invalid syntax {tokens[index]}')
                exit(1)
            index += 1
    return new_tokens


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")

    #add
    test("1+2")
    test("1.0+2")
    test("1+2.0")

    #sub
    test("1-2")
    test("2.0-2")
    test("1-2.0")

    #div
    test("1/2")
    test("1.0/2")
    test("1/2.0")
    test("1.0/2.0/3.0/4/5/2.0")

    #mul
    test("1*2.0")
    test("1.0*2.0")
    test("1.0*2")
    #when the answer becomes negative
    test("1*2.0-3")
    #check the ordering
    test("1+2.0*3")

    #mix of everything
    test("1.0*2.0/3.0+4-5/2.0")
    test("1.0-2.0+3.0/4-5*2.0")
    test("1.0+2.0/3.0+4*5*2.0")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
