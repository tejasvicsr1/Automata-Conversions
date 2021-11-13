# Assignment Report

---

## Automata Theory

---

### Tejasvi Chebrolu

2019114005

---

## Q1: Converting Regular Expression to NFA

- Obtaining the alphabet of NFA by removing `[ '(' , ')' , '*' , '+' ]` from the regular expression
- Next, going through the regular expression word by word
- If word belongs to alphabet:

    - If next word is `"*"`, create a loop by connecting the node to itself and add epsilon transition to a new node

    - Else, add a new node and connect the previous and new node

- If word is `"+"`:

    - If outside brackets, add epsilon transition from start to node for next branch and add this node to the **leaf** list.

- If word is `'('`:

    - Connect the previous node and new node and add new node to stack

- If word is `')'`:

    - If next character is `"*"`, add epsilon transition from previous node to last node in the stack 

    and vice- versa

---

## Q2: Converting NFA to DFA

- Initialize the states of the DFA as **powerset** of states of NFA
- Update the transition function as follows:

    - Each state in the DFA is a combination of states from the NFA

    - For each state $\in$ DFA , make a transition between two states if any of the sub-states had a connection in the original NFA

    - Start state of DFA = Start state of NFA

    - Finally, all states of DFA that have the final state of NFA as a sub-state are in final state of the DFA

---

## Q3: Converting DFA to Regular Expression

- As every DFA is an NFA , consider the DFA to be an NFA
- Add epsilon transition from a new dummy start node to original start node
- Add epsilon transition from all original final states to new dummy final state
- If multiple letters connect two nodes, create a new letter of the format `"( letter_1 + letter_2 + ... )"` to connect the two nodes
- Do reverse BFS from final state and calculate distance of each node from final state
- Consider a node in decreasing distance from final state:

    - If self loop exists for some state for letters `l1, l2, l3`, create new letter of the form `(l1+l2+l3)*`

    - Remove self loops from transition matrix

    - For connection between two nodes, if two different letters join node 1 to node 2, create a new transition of the form ( l1 + (self loop pattern for node 1) + l2)

- At the end, we only have transition between dummy start and dummy final ( call them different branches)
- Join all the branches using "+" concatenation operator to get the final regular expression

---

## Q4: Minimizing a DFA

- BFS from start state to find all the reachable states
- Next, remove the non reachable states from all the variables
- Use the table filling method for combining states
- Initialize as marked if states don't believe to same partition `(Q $\in$ F and Q $\notin$ F)`
- Repeat until no new states are marked

    - For combination of states which are not yet marked, if for any letter updated states after applying the letter are not same, mark this combination of states

- Combine the unmarked combinations
- Update all variables according to combined states