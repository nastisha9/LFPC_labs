INPUT = open('lab5.txt').read()
# split the string into an array of strings
input_array = INPUT.split('\n')


# function that returns a dictionary with splitted productions ({'S': ['dB], 'B':['D', 'DcB'] ...})
def productions(arr):
    map = {}
    for i in input_array:
        # split the rule
        x = i.split('->')
        # add the nonterminal to the map
        if not x[0] in map:
            # create an empty array for each nonterminal symbol
            map[x[0]] = []
        # apend to the array the corresponding terminals
        map[x[0]].append(x[1])
    return map


rules = productions(input_array)
# print(rules)

non_terminals = [i for i in rules.keys()]
terminals = []
for j in rules.values():
    for i in j:
        for k in i:
            if k.islower() and k not in terminals:
                terminals.append(k)
start_symbol = 'S'

# create first last arrays
index = []
first = []
last = []
for symbol in rules:
    index.append(symbol)
    to_search = []
    to_search.append(symbol)
    visited = []
    first_symbol = []

    # find the first array for each nonterminal
    idx = 0
    while idx < len(to_search):
        if to_search[idx] in rules:
            visited.append(to_search[idx])
            for rule in rules[to_search[idx]]:
                if rule[0] not in first_symbol:
                    first_symbol.append(rule[0])
                if rule[0] in non_terminals and rule[0] not in visited:
                    to_search.append(rule[0])
        idx += 1

    first.append(first_symbol)
    to_search = []
    to_search.append(symbol)
    visited = []
    last_symbol = []

    # find the last array for each nonterminal
    idx = 0
    while idx < len(to_search):
        if to_search[idx] in rules:
            visited.append(to_search[idx])
            for rule in rules[to_search[idx]]:
                if rule[-1] not in last_symbol:
                    last_symbol.append(rule[-1])
                if rule[-1] in non_terminals and rule[-1] not in visited:
                    to_search.append(rule[-1])
        idx += 1
    last.append(last_symbol)

# print the FIRST LAST table
print('Step 1. Find the First/Last table')
print('\t{:<5} {:<15} {:15}'.format('', 'FIRST', 'LAST'))
for i in range(4):
    print('\t{:<5}: {:<15} {:15}'.format(index[i], str(first[i]), str(last[i])))


def print_matrix(mat):
    for r in mat:
        for c in r:
            print('{:<7}'.format(str(c)), end='')
        print()


idx = 0
# create a dictionary with terminals and nonterminals
all_symbols = {}
for symbol in non_terminals:
    all_symbols[symbol] = idx
    idx += 1
for symbol in terminals:
    all_symbols[symbol] = idx
    idx += 1
all_symbols['$'] = idx
# def create_precedence_table()
precedence_table = [[[] for x in range(len(all_symbols) + 1)] for y in range(len(all_symbols) + 1)]
idx = 1
# Append the nonterminals
for symbol in non_terminals:
    precedence_table[0][idx].append(symbol)
    precedence_table[idx][0].append(symbol)
    idx += 1
# Append the terminals
for symbol in terminals:
    for ch in symbol:
        precedence_table[0][idx].append(ch)
        precedence_table[idx][0].append(ch)
    idx += 1
# Append the dollar sign and the corresponding symbols '<' and '>'
precedence_table[0][idx].append('$')
precedence_table[idx][0].append('$')
for i in range(1, idx):
    precedence_table[i][idx].append('>')
    precedence_table[idx][i].append('<')

# First Rule
# Find (=) rules by analysing each two symbols of a production
for key in rules:
    for prod in rules[key]:
        if len(prod) > 1:
            for idx in range(len(prod) - 1):
                first_symbol = prod[idx]
                second_symbol = prod[idx + 1]
                # Add the equal sign to the precedence table
                if '=' not in precedence_table[all_symbols[first_symbol] + 1][all_symbols[second_symbol] + 1]:
                    precedence_table[all_symbols[first_symbol] + 1][all_symbols[second_symbol] + 1].append('=')

# print_matrix(precedence_table)

# Second Rule
# Find (<) rules by analysing each two elements of a production
# terminal OR nonterminal < FIRST(nonterminal)
for key in rules:
    for prod in rules[key]:
        if len(prod) > 1:
            for idx in range(len(prod) - 1):
                first_symbol = prod[idx]
                second_symbol = prod[idx + 1]
                if second_symbol in non_terminals:
                    second_index = index.index(second_symbol)
                    for s in first[second_index]:
                        # Add the less sign to the precedence table
                        if '<' not in precedence_table[all_symbols[first_symbol] + 1][all_symbols[s] + 1]:
                            precedence_table[all_symbols[first_symbol] + 1][all_symbols[s] + 1].append('<')
# print_matrix(precedence_table)

# Third Rule
# Find (>) rules by analysing each two elements of a production
for key in rules:
    for prod in rules[key]:
        if len(prod) > 1:
            first_symbol = prod[idx]
            second_symbol = prod[idx + 1]
            # a) if nonterminal is followed by a terminal
            # LAST(nonterminal) > terminal
            if first_symbol in non_terminals and second_symbol in terminals:
                first_index = index.index(first_symbol)
                for s in last[first_index]:
                    # Add the greater sign to the precedence table
                    if '>' not in precedence_table[all_symbols[s] + 1][all_symbols[second_symbol] + 1]:
                        precedence_table[all_symbols[s] + 1][all_symbols[second_symbol] + 1].append('>')

            # b) if nonterminal is followed by a nonterminal
            # LAST(first_symbol) > (FIRST(second_symbol) in intersection with terminals)
            if first_symbol in non_terminals and second_symbol in non_terminals:
                first_index = index.index(first_symbol)
                second_index = index.index(second_symbol)
                for s1 in last[first_index]:
                    for s2 in first[second_index]:
                        if s2 in terminals:
                            if '>' not in precedence_table[all_symbols[s1] + 1][all_symbols[s2] + 1]:
                                precedence_table[all_symbols[s1] + 1][all_symbols[s2] + 1].append('>')

print('\n\nStep 2. Find the Simple Precedence Matrix')
print_matrix(precedence_table)

print('\n\nStep 3. Parse the word dbacbaa')

word = 'adabcd'
word = '$' + word + '$'
new_word = ''
for i in range(1, len(word)):
    new_word += word[i - 1] + precedence_table[all_symbols[word[i - 1]] + 1][all_symbols[word[i]] + 1][0]

new_word += '$'
print(new_word)
new_word_list = []
for ch in new_word:
    new_word_list.append(ch)
# print(new_word_list)

while new_word_list[2] != 'S' and len(new_word_list) != 5:
    start_index = 2
    end_index = 3
    while 1:
        if end_index < len(new_word_list) and new_word_list[end_index] != '<' and new_word_list[end_index] != '>':
            end_index += 1
        else:
            new_rule = new_word_list[start_index:end_index]
            new_rule = ''.join(new_rule)
            new_rule = new_rule.replace('=', '')

            is_rule = False

            for ch in rules:
                for rule in rules[ch]:
                    correct_rule = ''.join(rule)
                    if new_rule == correct_rule:
                        new_ch = ch
                        is_rule = True
            if is_rule:
                new_word_list[start_index] = new_ch
                if start_index > 0:
                    new_word_list[start_index - 1] = ' '
                if end_index < len(new_word_list):
                    new_word_list[end_index] = ' '
                del new_word_list[start_index + 1: end_index]
                break
            else:
                start_index = end_index + 1
                end_index += 2

    for idx in range((len(new_word_list) - 1) // 2):
        row = all_symbols[new_word_list[idx * 2]] + 1
        col = all_symbols[new_word_list[idx * 2 + 2]] + 1
        new_word_list[idx * 2 + 1] = precedence_table[row][col][0]
    print(''.join(new_word_list))
if len(new_word_list) == 5 and new_word_list[2] == 'S':
    print('Accepted')