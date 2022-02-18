import pandas as pd

grammar = [
    '0 a 1',
    '1 b 2',
    '2 c 0',
    '1 a 3',
    '3 b 2',
    '2 c 3 '
]

def parseGrammar(grammar):

    nfa = {}
    for grammarRules in grammar:
        rulePart = grammarRules.split(' ')

        if not rulePart[0] in nfa:
            nfa[rulePart[0]] = {}

        if not rulePart[1] in nfa[rulePart[0]]:
            nfa[rulePart[0]][rulePart[1]] = ''

        nfa[rulePart[0]][rulePart[1]] += rulePart[2]

    return nfa


def NFAtoDFA(nfa):

    states = []
    values = []

    for state in nfa:
        states.append(state)

    for state in nfa:
        for value in nfa[state]:

            if len(nfa[state][value]) > 1:
                if not nfa[state][value] in states:
                    states.append(nfa[state][value])
            else:
                if not nfa[state][value][0] in states:
                    states.append(nfa[state][value][0])

    for state in nfa:
        for value in nfa[state]:
            if not value in values:
                values.append(value)

    for state in states:
        if not state in nfa:
            newState = list(state)
            for value in values:
                val = []
                for st in newState:
                    if value in nfa[st]:
                        val.append(nfa[st][value])
                if not state in nfa:
                    nfa[state] = {}
                nfa[state][value] = ''.join(set(''.join(val)))
                states.append(''.join(set(''.join(val))))

    return nfa

print("\nThe initial NFA")
nfa = parseGrammar(grammar)
print(nfa)
NFA = pd.DataFrame(nfa)
NFA = NFA.fillna(" ")
print(NFA.transpose())

print("\nThe DFA after conversion")
dfa = NFAtoDFA(nfa)
print(dfa)
DFA = pd.DataFrame(dfa)
DFA = DFA.fillna(" ")
print(DFA.transpose())