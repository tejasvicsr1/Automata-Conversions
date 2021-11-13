from itertools import chain, combinations
import json
import sys

infile , outfile = sys.argv[1:3]

with open(infile) as inp:
	nfa = json.loads(inp.read())

def powerset(s):
	return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

dfa = {}

dfa['states'] = [list(i) for i in powerset(nfa['states'])]
t_func_states = dfa['states']
dfa['letters'] = nfa['letters']
flag = False
dfa['transition_function'] = []

for x in t_func_states:
    for letter in dfa["letters"]:
        flag = True
        update = set()
        for a in x:
            flag = False
            for y in nfa['transition_function']:
                if a == y[0] and letter == y[1]:
                    temp = y[2]
                    update.add(temp)
        temp = [list(sorted(x)), letter, list(sorted(update))]
        dfa['transition_function'].append(temp)

if type(nfa['start_states']) == list:
    dfa['start_states'] = [nfa['start_states']]
else:
    [nfa['start_states']]

dfa['final_states'] = []

for x in t_func_states:
    flag = True
    for y in nfa['final_states']:
        if y in x:
            temp = list(x)
            dfa['final_states'].append(temp)

with open(outfile, "w+") as out:
	out.write(json.dumps(dfa, indent=4))