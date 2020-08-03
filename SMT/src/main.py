import argparse
import sys
from pathlib import Path

from z3 import *
set_param("parallel.enable", True)


parser = argparse.ArgumentParser(description="Minizinc solver in python")
parser.add_argument("--instance",help="ABSOLUTE PATH of the instance file",default="")
parser.add_argument("--rot", help="Allow rotation",const=True,nargs="?",default=False,action="store")
parser.add_argument("--same-size",help="ACTIVATE lex_lesseq for avoid symmetries when rectangles with same size are present",const=True,nargs="?",default=False,action="store")
parser.add_argument("--out_dir", help="ABSOLUTE PATH of output folder",default="",action="store")

#For solving the toy problem inside the file
#args = parser.parse_args(["--rot"]);
args = parser.parse_args();

## Read the instance file
W = 0
H = 0
N = 0
widths = []
heights = []

if len(args.instance) > 0:
    with open(args.instance) as instances_file:
        for index,line in enumerate(instances_file):
            if ((line.strip())):    
                line = line.strip()
                if index == 0:
                    W = int(line.split()[0])
                    H = int(line.split()[1])
                elif index == 1:
                    N = int(line)
                else:
                    s = line.split()
                    widths.append(int(s[0]))
                    heights.append(int(s[1]))
else:
    ### Example with rotation and same sized rectangles
    # W = 5
    # H = 4
    # widths = [2,2,2,2,2,1]
    # heights = [2,2,2,2,1,2]
    # N = len(widths)
    
    ### Example with distict rectangles
    W = 6
    H = 5
    widths = [3,3,2,1]
    heights = [3,2,5,5]
    N = len(widths)

#-------------------
solver = Solver();
#-------------------
X = IntVector("x",N)
Y = IntVector("y",N)
Wi = IntVector("w",N)
Hi = IntVector("h",N)
#-------------------


if args.rot:
    INIT = And([Or(And(Wi[i]==widths[i],Hi[i]==heights[i]),And(Wi[i]==heights[i],Hi[i]==widths[i])) for i in range(N)])
else: 
    INIT = And([ And(Wi[i]==widths[i],Hi[i]==heights[i]) for i in range(N)])

BOUNDARIES = And([And(And(X[i]>=0,X[i]<=W-Wi[i]),And(Y[i]>=0,Y[i]<=H-Hi[i])) for i in range(N)])

NO_OVERLAP = And([ Or( X[i]+Wi[i]<=X[j],X[j]+Wi[j]<=X[i],Y[i]+Hi[i]<=Y[j],Y[j]+Hi[j]<=Y[i] ) for i in range(N) for j in range(N) if i<j ])


def lex_lesseq(X,Y):
    '''
    Decomposed lex_lesseq constraint
    INPUT:
    X: array
    Y: array
    RETURN:
    lex_lesseq clause
    '''
    final_and_list = list()
    for i in range(0,len(X)):        
            if i==0:
                final_and_list.append(X[i]<=Y[i])
            elif i==1:
                final_and_list.append(Implies(X[0]==Y[0],X[1]<=Y[1]))
            else:
                and1 = And( [X[k]==Y[k] for k in range(0,i)] )
                impl1 = Implies(and1,X[i]<=Y[i])
                final_and_list.append(impl1)
    final_and = And(final_and_list)
    return final_and

def same_size(i,j):
    return widths[i]==widths[j] and heights[i] == heights[j]

if args.same_size:
    NO_SYM_LEX_LESSEQ_list = list();
    for i in range(N):
        index_same_size = [ j for j in range(N) if same_size(i,j)]
        for i in index_same_size:
            if i>1:
                NO_SYM_LEX_LESSEQ_list.append(lex_lesseq([X[i-1],Y[i-1]],[X[i],Y[i]]))
    NO_SYM_LEX_LESSEQ = And(NO_SYM_LEX_LESSEQ_list)

SUM_OVER_HEIGHTS = ([ Sum([If(And(X[i]<=x,X[i]+Wi[i]>x),Hi[i],0) for i in range(N)]) == H for x in range(W) ])
SUM_OVER_WIDTHS = ([ Sum([If(And(Y[i]<=y,Y[i]+Hi[i]>y),Wi[i],0) for i in range(N)]) == W for y in range(H) ])


def print_solution(model):
    print(f"{W} {H}")
    print(N)
    for i in range(N):
        print(f"{model[Wi[i]]} {model[Hi[i]]} {model[X[i]]} {model[Y[i]]}")
    if len(args.out_dir)>0:
        out_name = f"{W}x{H}-out.txt"
        out_path = Path(args.out_dir) / out_name
        with open(out_path,'w') as out_file:
            out_file.writelines([\
                f"{W} {H}\n",
                f"{N}\n",
                *[f"{model[Wi[i]]} {model[Hi[i]]} {model[X[i]]} {model[Y[i]]}\n" for i in range(N)]
                ])


solver.append(INIT,BOUNDARIES,NO_OVERLAP)
if args.same_size: solver.append(NO_SYM_LEX_LESSEQ)
solver.append(*SUM_OVER_HEIGHTS,*SUM_OVER_WIDTHS)

if (solver.check() == sat):
    model = solver.model()
    print_solution(model)
else:
    print("unsat")
    print("maybe try --rot if rotation is possibile")
