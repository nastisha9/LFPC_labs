import string

INPUT = open('lab4.txt').read()
# split the string into an array of strings
input_array = INPUT.split('\n')


# initialize a dictionary with the split productions ({'S': ['bA', 'AC'], 'A': ['bS'] ...})
def prod(array):
    # create the dictionary map
    map = {}
    for i in input_array:
        x = i.split('->')
        # add the nonterminals to map
        if not x[0] in map:
            # create an empty array for all nonterminals
            map[x[0]] = []
        # append to the array the corresponding terminals
        map[x[0]].append(x[1])
    return map


def check_empty(map):
    for k, v in rules.items():
        for j in v:
            if j == '$':
                return True, k
    return False, 0


def get_absence_power_set(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in get_absence_power_set(seq[1:]):
            yield [seq[0]] + item
            yield item


# func to substitute epsilon
def subst_eps(str, substr, mask):
    result = []
    for m in mask:
        modified = str
        pos = 1
        for i in m:
            for _ in range(i):
                pos = modified.find(substr, pos - i)
            modified = modified[:pos] + modified[pos + 1:]
        result.append(modified)
    return result


# func that eliminates epsilon productions
def eliminate_empty_prod(map):
    production = map.copy()
    # check for epsilon productions
    check_eps, eps_key = check_empty(rules)
    if check_eps:
        production[eps_key].remove('$')
        if len(production[eps_key]) == 0:
            del production[eps_key]

    for key in production:
        for i, el in enumerate(production[key]):
            if eps_key in el:
                if eps_key in production:
                    # count the nr of nonterminal symbol that derives in eps, on the right side of each production, if exists
                    count = el.count(eps_key)
                    # the array of distinct appeareances of the nonterminal symbol on the right side
                    arr = []
                    for i in range(1, count + 1):
                        arr.append(i)
                    # create power subsets of absent nonterminals
                    sub_sets = []
                    for i in get_absence_power_set(arr):
                        sub_sets.append(i)
                    # substitute the nonterm that derives in eps, in order to get new productions
                    to_add = subst_eps(el, eps_key, sub_sets)[:-1]
                    # add the new productions
                    prod[key] = prod[key] + to_add
                else:
                    if (len(production[key][i])) == 1:
                        production[key].remove(eps_key)
                    else:
                        production[key][i] = el.replace(eps_key, '')
    check_eps, eps_key = check_empty(prod)
    return production


# func that checks unit productions
def check_unit(key, map):
    for el in map[key]:
        if len(el) == 1 and el in map:
            # if X->Y, return True and Y
            return True, el
    return False, 0


# func that removes unit prod and adds new ones
def remove(key, initial_value, map):
    is_unit, unit = check_unit(initial_value, map)

    if is_unit:
        map = remove(initial_value, unit, map)

    # eliminate the unit production
    map[key].remove(initial_value)
    # add the new productions after substitution
    map[key] = map[key] + map[initial_value]
    return map


# func that eliminates all unit prod
def eliminate_unit_prod(map):
    production = map.copy()
    # traverse the keys S, A, B, C
    for key in production:
        # check for unit productions
        is_unit, unit = check_unit(key, production)
        # remove them
        if is_unit:
            production = remove(key, unit, production)
    return production


# func that eliminates inaccessible symbols
def eliminate_inaccessible_symb(map):
    production = map.copy()
    accessed_keys = set()

    for key, value in production.items():
        for i in value:
            for symbol in i:
                # fint the accesses nonterms
                if symbol in production:
                    accessed_keys.add(symbol)

    # find and delete the inaccess symbl
    for key in list(production):
        if key not in accessed_keys:
            del production[key]
    return production


# func that eliminates nonproductive symbls
def eliminate_nonproductive_symb(map):
    production = map.copy()
    productive_symbols = set()
    # find the nonterms that derive in a terminal
    for key in production:
        for el in production[key]:
            if (len(el) == 1) and (el not in production):
                productive_symbols.add(key)

    i = 1
    while i:
        for key in production:
            if key in productive_symbols:
                continue
            for el in prod[key]:
                # check each letter in part from left side of production
                for letter in el:
                    if letter in productive_symbols:
                        # if the letter (nonterm symb) is in the set, we add the key of this production
                        # as it has a path from one to another nontem
                        productive_symbols.add(key)
                        i += 1
        i -= 1

    for key in list(production):
        # delete the key and values od a nonproductive
        if key not in productive_symbols:
            del production[key]

            for innerkey in list(production):
                for el in production[innerkey]:
                    if key in el:
                        production[innerkey].remove(el)
    return production


def new_symbol(pos, map):
    letters = string.ascii_uppercase
    while letters[pos] in map:
        pos -= 1
    return letters[pos], pos


def has_terminal(str):
    for letter in str:
        if letter in string.ascii_lowercase:
            return True
    return False


# func that normalizes the grammar
def chomsky(map):
    production = map.copy()
    temp = {}
    terminals = string.ascii_lowercase
    letters_counter = len(string.ascii_uppercase) - 1

    u = 1
    while u:
        for key in list(production):
            for i, el in enumerate(production[key]):
                # letter = el[1:]
                if len(el) > 2:
                    if el in temp:
                        # if the el exists in the dictionary temp, which contains the new symbols and their productions, ex:{'AabB':'ZB'}
                        # then it simply assigns
                        production[key][i] = temp[el]
                    else:
                        # otherwise it creates a new nonterminal symbol
                        new_letter, letters_counter = new_symbol(letters_counter, production)
                        # assigns it in temp{}
                        temp[el] = el[0] + new_letter
                        # reduces the length by one of the right side of production rule
                        production[new_letter] = [el[1:]]
                        production[key][i] = temp[el]
                        u += 1
        u -= 1
    # temp = {}
    for key in list(production):
        for i, el in enumerate(production[key]):
            if (len(el) == 2) and has_terminal:
                if el in temp:
                    # if the el exists in the dictionary temp, which contains the new symbols and their productions, ex:{'AabB':'ZB'}
                    # then it simply assigns
                    production[key][i] = temp[el]
                else:
                    for letter in el:
                        if letter in terminals:
                            if letter in temp:
                                production[key][i] = production[key][i].replace(letter, temp[letter])
                            else:
                                # otherwise creates a new nonterminal symbol
                                new_letter, letters_counter = new_symbol(letters_counter, production)
                                # assigns it in temp{}
                                temp[letter] = new_letter
                                production[temp[letter]] = [letter]
                                # replaces the terminals in productions of length = 2 with new nonterminal
                                production[key][i] = production[key][i].replace(letter, temp[letter])
                    temp[el] = production[key][i]
    # delete dulpications by converting list to set and then back to list
    for key, value in production.items():
        production[key] = list(set(value))
    return production


rules = prod(input_array)
rules = eliminate_empty_prod(rules)
rules = eliminate_unit_prod(rules)
rules = eliminate_inaccessible_symb(rules)
rules = eliminate_nonproductive_symb(rules)
rules = chomsky(rules)

print('The Chomsky Normal Form of the grammar:')
for key in rules:
    print(key, '->', rules[key])
