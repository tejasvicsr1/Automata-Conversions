# Skipping variables so far.
from itertools import chain, combinations
import sys
import json

infile = sys.argv[1]
outfile = sys.argv[2]

f = open(infile)
inp = json.loads(f.read())

stack = []
regex = inp['regex']
print(regex)
letters = list(set(regex) - set(['(',')','*','+']))
# letters = list(set(regex) - set(['(',')','*','+']))


nfa = {}
states = []
nfa['letters'] = letters
counter = 0

def get_node_name():
    global counter
    global states
    ret = 'Q' + str(counter)
    states.append(ret)
    counter = 1 + counter
    return ret

skipnext = False
start_node = get_node_name()
nfa['start_states'] = start_node
orphans = []
prev_node = get_node_name()
nfa['transition_function'] = [[nfa['start_states'] , '$' , prev_node]]
branches = [[]]
regex_len = len(regex)

for i in range(regex_len):
    if skipnext:
        sums = 1
        skipnext = not skipnext
        continue
    
    n_regex_len = len(regex) - 1
    char = regex[i]

    if i < n_regex_len:
        nextchar = regex[i + 1]
    else:
        None
    if i > 0:
        lastchar = regex[i - 1]
    else:
        None
    

    if char in letters:
        if nextchar == "*":
            temp = [prev_node , char , prev_node]
            nfa['transition_function'].append(temp)
            cur_node = get_node_name()
            temp = [prev_node , '$' , cur_node]
            nfa['transition_function'].append(temp)
            skipnext = True
        else:
            cur_node = get_node_name()
            temp = [prev_node , char , cur_node]
            nfa['transition_function'].append(temp)
        prev_node = cur_node
    elif char == '(':
        cur_node = get_node_name()
        temp = [prev_node , '$' , cur_node]
        nfa['transition_function'].append(temp)
        stack.append(cur_node)
        prev_node = cur_node
        branches.append([])
    elif char == ')':
        stack_len = len(stack)
        if branches[stack_len]:
            cur_node = get_node_name()
            for node in branches[len(stack)] + [prev_node]:
                temp = [node , '$' , cur_node]
                nfa['transition_function'].append(temp)
            prev_node = cur_node
            branches.pop()
        if nextchar == '*':
            skipnext = True
            temp_1 = [prev_node , '$' , stack[-1]]
            temp_2 = [stack[-1] , '$' , prev_node]
            nfa['transition_function'].append(temp_1)
            nfa['transition_function'].append(temp_2)
        stack.pop()

    elif char == '*':
        temp = None
        print("Error")
        exit()

    elif char == '+':
        stack_len = len(stack)
        if stack_len == 0:
            orphans.append(prev_node)
            prev_node = get_node_name()
            temp = [start_node , '$' , prev_node]
            nfa['transition_function'].append(temp)
        else:
            branches[len(stack)].append(prev_node)
            prev_node = stack[-1]

for node in orphans:
    temp = [node , '$' , prev_node]
    nfa['transition_function'].append(temp)

nfa['start_states'] = [nfa['start_states']]
nfa['final_states'] = [prev_node]
nfa['states'] = states

with open(outfile, "w+") as out:
	out.write(json.dumps(nfa, indent=4))



            