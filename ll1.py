# Author : Vasu Gondaliya

def findFirst(productions, terminal, non_terminal):
    first = dict()
    first_found = dict()
    for x in terminal:
        first[x] = [x]
    for x in non_terminal:
        first[x] = []
        first_found[x] = 1
    for x in productions:
        temp_first = []
        for y in productions[x]:
            if y[0] in terminal:
                temp_first.append(y[0])
            else:
                first_found[x] = 0
        if(first_found[x] == 1):
            first[x] = list(set(temp_first))
    while(0 in list(first_found.values())):
        for x in productions:
            if(first_found[x] == 0):
                temp_first = []
                x_found = 1
                for y in productions[x]:
                    for z in y:
                        if z in terminal:
                            temp_first.append(z)
                            break
                        else:
                            if(first_found[z] == 0):
                                x_found = 0
                                break
                            else:
                                temp_first += [w for w in first[z] if w != '#']
                                if '#' in first[z]:
                                    if z == y[-1]:
                                        temp_first.append('#')
                                else:
                                    break
                    if x_found == 0:
                        break
                if x_found == 1:
                    first[x] = list(set(temp_first))
                    first_found[x] = 1
    return first


def findFollow(productions, terminal, non_terminal, first):
    follow = dict()
    follow_found = dict()
    t_productions = dict()
    for x in non_terminal:
        follow[x] = []
        follow_found[x] = 0
        t_productions[x] = []
    follow[non_terminal[0]].append('$')

    for x in productions:
        for y in range(len(productions[x])):
            for z in range(len(productions[x][y])):
                if productions[x][y][z] in non_terminal:
                    t_productions[productions[x][y][z]].append([x, y, z])
    while(0 in list(follow_found.values())):
        for x in t_productions:
            temp_follow = []
            x_found = 1
            for y in t_productions[x]:
                for z_ind, z in enumerate(productions[y[0]][y[1]][y[2]+1:], start=y[2]+1):
                    for w in first[z]:
                        if '#' != w:
                            temp_follow.append(w)
                    if '#' not in first[z]:
                        break
                    else:
                        if z_ind == len(productions[y[0]][y[1]])-1:
                            if follow_found[z] == 1:
                                temp_follow += follow[z]
                            elif z != x:
                                x_found = 0
                if y[2] == len(productions[y[0]][y[1]])-1:
                    if follow_found[y[0]] == 1:
                        temp_follow += follow[y[0]]
                    elif y[0] != x:
                        x_found = 0
                if x_found == 0:
                    break
            if x_found == 1:
                follow_found[x] = 1
                follow[x] = list(set(follow[x]+temp_follow))
    return follow


def findParseTable(productions, terminal, non_terminal, first, follow):
    parse_table = dict()
    for x in non_terminal:
        for y in terminal:
            if y != '#':
                parse_table[(x, y)] = []
    for x in productions:
        for y in productions[x]:
            if y == ['#']:
                for z in follow[x]:
                    parse_table[(x, z)] = [x, y]
            else:
                for z in first[y[0]]:
                    if z != '#':
                        parse_table[(x, z)] = [x, y]
    return parse_table


def stringAccept(inp_string, productions, terminal, non_terminal, first, follow, parse_table):
    inp = list(inp_string)
    inp.append('$')
    stack = ['$', 'S']
    changed = 1
    while(changed == 1 and len(inp) > 0 and len(stack) > 0):
        print('S : ' + str(stack))
        print('I : ' + str(inp))
        changed = 0
        if stack[-1] in non_terminal:
            changed = 1
            stack_last = stack.pop()
            for x in reversed(parse_table[(stack_last, inp[0])][1]):
                if x != '#':
                    stack.append(x)
        elif stack[-1] == inp[0]:
            changed = 1
            stack.pop()
            inp.pop(0)
    if len(inp) > 0 or len(stack) > 1:
        return False
    else:
        return True


no_productions = int(
    input("Number of Productions of type (A -> a B | C | #): "))
productions = dict()
print("Enter Productions (# for epsilon) : ")
for i in range(no_productions):
    production = input().split()
    rhs = []
    rhsx = []
    for j in range(2, len(production)):
        if(production[j] != '|'):
            rhsx.append(production[j])
        else:
            rhs.append(rhsx)
            rhsx = []
    rhs.append(rhsx)
    productions[production[0]] = rhs

terminal = []
non_terminal = list(productions.keys())

for x in productions:
    for y in productions[x]:
        for z in y:
            if z not in non_terminal:
                terminal.append(z)
terminal = list(set(terminal))
first = findFirst(productions, terminal, non_terminal)
print("First : ")
for x in first:
    if x in non_terminal:
        print(x + " : ", end="")
        print(first[x])
terminal.append('$')
follow = findFollow(productions, terminal, non_terminal, first)
print("Follow : ")
for x in follow:
    print(x + " : ", end="")
    print(follow[x])
parse_table = findParseTable(
    productions, terminal, non_terminal, first, follow)
print("Parse Table : ")
for x in non_terminal:
    print(x + " : ")
    for y in terminal:
        if y != '#':
            print(y+" : "+str(parse_table[(x, y)]))
inp_string = input("Enter string to check acceptance : ")
if(stringAccept(inp_string, productions, terminal, non_terminal, first, follow, parse_table) == True):
    print(inp_string + " accepted by grammar")
else:
    print(inp_string + " rejected by grammar")

# Grammar :
# S -> A S b | C
# A -> a
# C -> c C | #
# Input String : aaccbb
