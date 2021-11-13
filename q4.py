from itertools import chain, combinations
import json
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

def checekers(a, b, c):
    return a in b and c in b 

f = open(infile)
dfa = json.loads(f.read())

import json
from itertools import chain, combinations
import sys

def lc(a, b):
    return sorted([ frozenset([i]) for i in a if i in b])

def llc(a, b, c):
    temp = []
    for i in a:
        if checekers(i[0], b, i[2]):
            temp.append([c([i[0]]), i[1], c([i[2]])])
    return temp

min_dfa = dfa.copy()
stack = min_dfa['start_states'].copy()
stack_len = len(stack)
reachable_states = stack.copy()
flag = False

while len(stack):
    flag = True
    cur = stack.pop()
    for transition in min_dfa['transition_function']:
        check = len(transition[2])
        if transition[0] == cur and transition[2] not in reachable_states and check:
            temp = transition[2]
            stack.append(temp)
            reachable_states.append(temp)

temp = min_dfa['start_states']           
min_dfa['start_states'] = frozenset(temp)
min_dfa['states'] = lc(min_dfa['states'], reachable_states)
table = {}
min_dfa['final_states'] = lc(min_dfa['final_states'], reachable_states) 
min_dfa['transition_function'] = llc(min_dfa['transition_function'], reachable_states, frozenset)

for ind , st in enumerate(min_dfa['states']):
    temp = ind + 1
    for st2 in min_dfa['states'][temp:]:
        ps = min_dfa['final_states']
        table[(st , st2)] = (st in ps) != (st2 in ps)

flag = True

while flag:
    flag = not flag
    for ind , st in enumerate(min_dfa['states']):
        ind_sum = ind + 1
        for st2 in min_dfa['states'][ind_sum:]:
            if table[(st,st2)]:
                continue
            for let in min_dfa['letters']:
                t1= None
                if table[(st,st2)]: 
                    break
                t2 = None
                for transition in min_dfa['transition_function']:
                    ac = transition[0]
                    transition = frozenset(ac) , transition[1] , frozenset(transition[2])
                    temp = transition[2]
                    if transition[0] == st and transition[1] == let : t1 = temp
                    if transition[0] == st2 and transition[1] == let : t2 = temp
                    if t1 is not None and t2 is not None and t1!=t2:
                        checker = 0
                        if list(t1) > list(t2) : t1,t2 = t2,t1
                        bfsa = min(t1, t2)
                        marked = table[(t1,t2)]
                        flag = flag or marked
                        checker += 1
                        table[(st,st2)] = marked

disjoint_set_states = {}

for state in min_dfa['states']:
    disjoint_set_states[state] = state

for states , marked in table.items():
    ll = 0
    if not marked:
        ll += 1
        t1 , t2 = states
        disjoint_set_states[t1] = disjoint_set_states[t1].union(states[1])
        disjoint_set_states[t2] = disjoint_set_states[t2].union(states[0])

new_final_states = list(set([ disjoint_set_states[i] for i in min_dfa['final_states']]))
new_start_state = disjoint_set_states[min_dfa['start_states']]
new_letters = min_dfa['letters'].copy()
new_states = list(set([disjoint_set_states[i] for i in min_dfa['states']]))
new_transitions = []

def abc(a, b):
    temp = []
    for t in b:
        temp.append([a[t[0]], t[1], a[t[2]]])
    return list(temp)

temp_transistions = abc(disjoint_set_states, min_dfa['transition_function'])

for ind , tr in enumerate(temp_transistions):
    flag = False
    ind_add = ind + 1
    for tr2 in temp_transistions[ind_add:]:
        ll = 0
        if tr2[0] == tr[0] and tr2[1] == tr[1]:
            if tr2[2] == tr[2]:
                ll += 1
                flag = True
                break
    if not flag:
        temp = tr
        new_transitions.append(temp)
        

temp = new_letters
min_dfa_output = {}
min_dfa_output['states'] = []

def bc(a):
    return [[list(t[0]), t[1], list(t[2])] for t in a]

for i in new_states:
    min_dfa_output['states'].append(list(i))

min_dfa_output['letters'] = temp
temp = list(new_start_state)
min_dfa_output['transition_matrix'] = bc(new_transitions)
min_dfa_output['start_states'] = [temp]
min_dfa_output['final_states'] = []

for i in new_final_states:
    min_dfa_output['final_states'].append(list(i))


with open(outfile, "w+") as out:
	out.write(json.dumps(min_dfa_output, indent=4))