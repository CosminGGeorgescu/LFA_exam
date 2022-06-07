f = open('config_file_2.txt', 'r')
input = "_0110#0110_"
#first tape
tape1 = [x for x in input]
#second tape
tape2 = [x for x in input]
#head
i = 0
#possible moves the head can make
moves = ['L', 'R', 'S']
#set of states
states = []
#input alphabet
sigma = []
#tape alphabet
gamma = []
#start state
start = ''
#accept states
accept = []
#reject states
reject = []
#delta function
delta = {}
while line := f.readline():
    if "States" in line:
        while "End" not in (line := f.readline()):
            states.append(line[:len(line) - 1])
    elif "Sigma" in line:
        while "End" not in (line := f.readline()):
            sigma.append(line[:len(line) - 1])
    elif "Gamma" in line:
        while "End" not in (line := f.readline()):
            gamma.append(line[:len(line) - 1])
    elif "Start" in line:
        start = (line := f.readline())[:len(line) - 1]
        states.append(start)
    elif "Accept" in line:
        while "End" not in (line := f.readline()):
            accept.append(line[:len(line) - 1])
            states.append(accept[len(accept) - 1])
        #check if the accept state is same as reject one
        if len(reject) and accept[len(accept) - 1] in reject:
            exit("Accept state can not reject state at the same time")
    elif "Reject" in line:
        while "End" not in (line := f.readline()):
            reject.append(line[:len(line) - 1])
            states.append(reject[len(reject) - 1])
        #same as 5 lines above
        if len(accept) and reject[len(reject) - 1] in accept:
            exit("Accept state can not reject state at the same time")
    elif "Delta"in line:
        while "End" not in (line := f.readline()):
            line = line.split(' ')
            #remove \n from the last element of line 
            line[len(line) - 1] = line[len(line) - 1][:len(line[len(line) - 1]) - 1]
            #check if current state and future state of transition is valid
            if (line[0] not in states) or (line[3] not in states):
                exit("Invalid transition state")
            #check if read and to-be-written symbols are valid
            if ((line[1] not in sigma) and (line[1] not in gamma)) or ((line[2] not in sigma) and (line[2] not in gamma)) or ((line[4] not in sigma) and (line[4] not in gamma)) or ((line[5] not in sigma) and (line[5] not in gamma)): #   
                exit("Invalid transition symbols")
            #check if indicated move is valid
            if line[6] not in moves:
                exit("Invalid move")
            #argument of delta function
            arg = (line[0], line[1], line[2]) #
            #value of delta[arg]
            value = [line[3], line[4], line[5], line[6]] #
            delta[arg] = value
#check if there is a start, accept and reject states
if (not len(start)) or (not len(accept)) or (not len(reject)):
    exit("INVALID CONFIG")
#check if there is an end-of-input symbol in gamma
if '_' not in gamma:
    exit("_ absent from gamma")
#check if intersection of sigma and gamma is void
for symbol in gamma:
    if symbol in sigma:
        print(symbol)
        exit(f"Ambiguous definition of {symbol}")
state = start
i = 0
while (state not in accept) and (state not in reject):
    rule = delta[(state, tape1[i], tape2[i])]
    tape1[i] = rule[1]
    tape2[i] = rule[2]
    if rule[3] == 'L':
        if i != 0:
            i = i - 1
    elif rule[3] == 'R':
        i = i + 1
    state = rule[0]
if state in accept:
    exit("Input accepted")
else:
    exit("Input rejected")