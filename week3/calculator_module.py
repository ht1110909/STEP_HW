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

def read_open(line, index):
    token = {'type': 'LPAREN'}
    return token, index+1

def read_close(line, index):
    token = {'type': 'RPAREN'}
    return token, index+1

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
        elif line[index] == '(':
            (token, index) = read_open(line, index)
        elif line[index] == ')':
            (token, index) = read_close(line, index)
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
    process_paren(tokens)
    process_divmul(tokens)
    process_addsub(tokens)
    return tokens[0]['number']

def process_paren(tokens):
    index = 0
    while index < len(tokens):
        #find the first closing parentheses
        if tokens[index]['type'] == 'RPAREN':
            subindex = index
            #going backward to find the first open paren == matching lparen
            while tokens[subindex]['type'] != 'LPAREN':
                subindex -= 1
            #evaluate the value in the paren
            result = evaluate(tokens[subindex+1:index])
            #change the paren stuff to the number
            tokens[subindex:index+1] = [{'type': 'NUMBER', 'number': result}]
            #iterate through the tokens again
            index = 0
        else:
            index+=1

def process_divmul(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] in ('MULTIPLY', 'DIVIDE'):
            #grab the neighboring numbers to compute
            first_num = tokens[index-1]['number']
            #since we process paren first we know it's always a number
            second_num = tokens[index+1]['number']
            if tokens[index]['type'] == 'MULTIPLY':
                result = first_num*second_num
            else:
                result = first_num/second_num
            #change the three tokens into one computed value
            tokens[index-1:index+2] = [{'type': 'NUMBER', 'number': result}]
            #since the tokens got mutated, start scanning from the beginning
            index = 0
        else:
            index+=1


def process_addsub(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] in ('PLUS', 'MINUS'):
            #grab the neighboring numbers to compute
            first_num = tokens[index-1]['number']
            #since we process paren first we know it's always a number
            second_num = tokens[index+1]['number']
            if tokens[index]['type'] == 'PLUS':
                result = first_num+second_num
            else:
                result = first_num-second_num
            #change the three tokens into one computed value
            tokens[index-1:index+2] = [{'type': 'NUMBER', 'number': result}]
            #since the tokens got mutated, start scanning from the beginning
            index = 0
        else:
            index+=1

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
    test("1-2-3")


    #div
    test("1/2")
    test("1.0/2")
    test("1/2.0")
    test("1.0/2.0/3.0/4/5/2.0")

    #mul
    test("1*2.0")
    test("1.0*2.0")
    test("1.0*2")
    test("0.5*0.5")
    #when the answer becomes negative
    test("1*2.0-3")
    #check the ordering
    test("1+2.0*3")
    test("10-2*3+1")

    #mix of everything
    test("1.0*2.0/3.0+4-5/2.0")
    test("1.0-2.0+3.0/4-5*2.0")
    test("1.0+2.0/3.0+4*5*2.0")
    test("1.0*2.0+3.0*4")

    #paren
    test("(1+2)/3")
    test("(3.0+4*(2-1))/5")
    test("(1+2)/3*(4-5)")
    test("(1+(2-4))/3")
    test("4*(2*1)")

    #edge
    test("42")
    test("(42)")
    test("0*0")
    test("0+0")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
