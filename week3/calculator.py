while True:
    line = input()
    answer = 0
    index = 0
    operand = ""
    isPeriod = False

    while index < len(line):
        number = 0
        if line[index].isdigit():
            while index < len(line) and (line[index].isdigit() or line[index] == '.'):
                if line[index] == '.':
                    isPeriod = True
                number = number * 10 + int(line[index])
                index += 1
            if operand == "add":
                answer += number
            elif operand == "minus":
                answer -= number
            else:
                answer += number
        elif line[index] == '+':
            index += 1
            operand = "add"
        elif line[index] == '-':
            index += 1
            operand = "minus"
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
    print("answer = %d\n" % answer)
