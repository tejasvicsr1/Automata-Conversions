from itertools import chain, combinations
from collections import defaultdict
import json
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

f = open(infile)

nfa = json.loads(f.read())
nfa = nfa.copy()
stack = nfa['start_states'].copy()
reachable_states = stack.copy()

def aa(a, b):
    return sorted([i for i in a if i in b])

def get_node_name():
    global counter
    global network_nfa
    counter += 1
    ret = 'Q' + str(counter)
    network_nfa['states'].append(ret)
    return ret

while len(stack):
    flag = False
    cur = stack.pop()
    for transition in nfa['transition_function']:
        t_len = len(transition[2])
        if transition[0] == cur and transition[2] not in reachable_states and t_len:
            temp = transition[2]
            stack.append(temp)
            reachable_states.append(temp)

temp = nfa['start_states']
nfa['start_states'] = temp
nfa['states'] = aa(nfa['states'], reachable_states)
orig_states = nfa['states'].copy()
nfa['final_states'] = aa(nfa['final_states'], reachable_states)
counter = len(nfa['states'])
temp = []

for i in nfa['transition_function']:
    if i[0] in reachable_states and i[2] in reachable_states:
        temp.append([i[0],i[1] ,i[2]])
nfa['transition_function'] = temp

network_nfa = nfa.copy()
start_node = get_node_name()
temp = [start_node, '$', network_nfa['start_states'][0]]
network_nfa['transition_function'].append(temp)
network_nfa['start_states'] = start_node
end_node = get_node_name()

for final in network_nfa['final_states']:
    temp = [final, '$', end_node]
    network_nfa['transition_function'].append(temp)
network_nfa['final_states'] = [end_node]

for src in network_nfa['states']:
    src_transition = []
    for i in network_nfa['transition_function']:
        if i[0] == src:
            src_transition.append(i)
    for dest in network_nfa['states']:
        chars = []
        flag = False
        for trans in src_transition:
            if dest == trans[2]:
                temp = trans[1]
                chars.append(temp)
        if len(chars):
            if len(chars) <= 1:
                chars = '+'.join(chars)
            else:
                chars = '(' + '+'.join(chars) + ')'
            temp = [src, chars, dest]
            network_nfa['transition_function'].append(temp)

new_transitions = []
p_nodes = orig_states.copy()

for ind, tr in enumerate(network_nfa['transition_function']):
    flag = False
    ind_sum = ind + 1
    for tr2 in network_nfa['transition_function'][ind_sum:]:
        ll = 0
        if tr2[0] == tr[0] and tr2[1] == tr[1]:
            if tr2[2] == tr[2]:
                ll += 1
                flag = True
                break
    if not flag:
        temp = tr
        new_transitions.append(temp)

maxdist = 1e10
network_nfa['transition_function'] = new_transitions.copy()
nodefinaldist = {}

for state in network_nfa['states']:
    nodefinaldist[state] = maxdist

tocheck = list(network_nfa['states'])
term_nodes = []
nodefinaldist[network_nfa['final_states'][0]] = 0
i = 0
tocheck.remove(network_nfa['final_states'][0])

while len(tocheck) and i < float('inf'):
    i = i + 1
    for node in tocheck:
        dests = set([i[2]for i in network_nfa['transition_function'] if i[0] == node])
        # dests = set(dests)
        dest_len = len(dests)
        if dest_len == 0:
            tocheck.remove(node)
        else:
            flag = False
            mind = min([nodefinaldist[i] for i in dests])
            if mind == maxdist:
                if set(dests) == set([node]):
                    term_nodes.append(node)
                    flag = True
                    tocheck.remove(node)
            else:
                temp = mind + 1
                nodefinaldist[node] = temp
                tocheck.remove(node)

temp = []
for node in p_nodes:
    if node not in term_nodes:
        temp.append(node)
p_nodes = temp

temp = []

for tr in network_nfa['transition_function']:
    if tr[0] not in term_nodes and tr[2] not in term_nodes:
        temp.append(tr)
network_nfa['transition_function'] = temp
p_nodes.sort(key=lambda x: nodefinaldist[x], reverse=True)
flag = False

for node in p_nodes:
    flag = True
    src_transition = defaultdict(set)
    network_nfa['states'].remove(node)
    for tr in network_nfa['transition_function']:
        if tr[0] == node:
            temp = tr[2]
            src_transition[tr[1]].add(temp)

    loops = []
    for letter in src_transition:
        if node in src_transition[letter]:
            flag = False
            if letter == '$':
                flag = True
            else:
                loops.append(letter)
    cc = 0
    loopreg = '+'.join(loops)
    if len(loopreg) > 1:
        if not (loopreg[0] == '(' and loopreg[-1] == ')'):
            loopreg = '(' + loopreg
            loopreg = loopreg + ')*'
    elif len(loopreg) >= 1:
        loopreg = loopreg + '*'

    for letter in src_transition.copy():
        ll = 0
        if src_transition[letter] == set([node]):
            ll += 1
            del src_transition[letter]
        elif node in src_transition[letter]:
            ll -= 1
            src_transition[letter].remove(node)

    # network_nfa['transition_function'] = []
    temp = []
    for tr in network_nfa['transition_function']:
        if tr[0] != node:
            temp.append(tr)
    network_nfa['transition_function'] = temp
    temp_transition = network_nfa['transition_function'].copy()

    for src in network_nfa['states']:
        flag = False
        src_transition2 = defaultdict(set)
        for tr in temp_transition:
            temp = tr[2]
            if tr[0] == src:
                src_transition2[tr[1]].add(temp)
        for letter in src_transition2:
            flag = True
            dest_list = src_transition2[letter]
            if node in dest_list:
                dest_list.remove(node)
                ldl = len(dest_list)
                if ldl == 0:
                    temp = []
                    for tr in network_nfa['transition_function']:
                        if not (tr[0]== src and tr[1]==letter):
                            temp.append(tr)
                    network_nfa['transition_function'] = temp
                for letter2 in src_transition:
                    temp = letter + loopreg + letter2
                    for dest in src_transition[letter2]:
                        if not(src == dest and temp == '$'):
                            btemp = [src , letter + loopreg + letter2 , dest]
                            network_nfa['transition_function'].append(btemp)

temp = []

for tr in network_nfa['transition_function']:
    if tr[0] == network_nfa['start_states']:
        temp.append(tr[1])
branches = temp

if len(branches) != 1:
    regex = '+'.join(branches)
else :
    regex = branches[0]

output = {}
output['regex'] = regex

with open(outfile, "w+") as out:
	out.write(json.dumps(output, indent=4))