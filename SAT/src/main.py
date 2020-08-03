from z3 import *
import argparse
from math import log2,floor




parser = argparse.ArgumentParser(description="Minizinc solver in python")
parser.add_argument("--instance",help="ABSOLUTE PATH of the instance file",default="")
parser.add_argument("--out_dir", help="ABSOLUTE DIR for output file",default="")

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
     #test constants
    W = 5
    H = 4
    N = 4
    widths = [4,3,2,1]
    heights = [2,2,2,2]
    N = len(widths)

bit_per_number = int(log2(max(W,H)))+1+2 #In order to take into account overflow
# had problem with only +1

X = [ BoolVector(f"x_{x}",bit_per_number) for x in range(W) ]
Y = [ BoolVector(f"y_{y}",bit_per_number) for y in range(H) ]

Wi = [ BoolVector(f"w_{w}",bit_per_number) for w in range(N) ]
Hi = [ BoolVector(f"h_{h}",bit_per_number) for h in range(N) ]

WB = [ W-widths[i] for i in range(N)  ]
HB = [ H-heights[i] for i in range(N) ]


solver = Solver()

def int_to_bits(num,max_width):
    return format(num,'b').zfill(max_width)

def bits_to_bool(bits):
    return [True if bits[i]=='1' else False for i in range(len(bits))]

def int_to_bools(num):
    bits = int_to_bits(num,bit_per_number)
    return bits_to_bool(bits)
def int_to_bools2(num,max_width):
    bits = int_to_bits(num,max_width)
    return bits_to_bool(bits)

def assign_bits_to_z3_var(z3_var,bits_var):
    return And([ z3_var[bit] == True if bits_var[bit]=='1' else z3_var[bit] == False for bit in range(bit_per_number) ])

INIT_Wi_Hi_list = list()
for i in range(N):
    w = int_to_bits(widths[i],bit_per_number)
    h = int_to_bits(heights[i],bit_per_number)
    and_w = assign_bits_to_z3_var(Wi[i],w)
    and_h = assign_bits_to_z3_var(Hi[i],h)
    INIT_Wi_Hi_list.extend([and_w,and_h])
INIT_Wi_Hi = And(INIT_Wi_Hi_list)

def _bool_lesseq(a,b):
    return Or(And(Not(a),Not(b)),And(a,b),And(Not(a),b))

def _bool_greateq(a,b):
    return Or(And(Not(a),Not(b)),And(a,b),And(a,Not(b)))

def bool_lesseq(first,other):
    if isinstance(first,int):
        A=int_to_bools(first)
    else:
        A=first
    if isinstance(other,int):
        B=int_to_bools(other)
    else:
        B=other
    bits = len(A)
    return And([_bool_lesseq(A[i],B[i]) for i in range(bits) ])

def bool_greateq(A,other):
    if isinstance(other,int):
        B=int_to_bools(other)
    else:
        B=other
    return And([_bool_greateq(A[i],B[i]) for i in range(bit_per_number) ])

def add_bool(l,r):
    '''
    l,r: array of bools
    '''
    if isinstance(l,int):
        A = int_to_bools(l)
    else:
        A = l
    if isinstance(r,int):
        B = int_to_bools(r)
    else:
        B = r

    assert(len(A)==len(B))

    bits  = len(A)

    
    and_list = list()
    
    out_bool = BoolVector("o",bits)
    C = BoolVector("c",bits)
    
    and_list.append(Not(C[0]))
    and_list.append(Not(C[-1]))

    for i in reversed(range(bits)):
        (a,b,c) = ( A[i],B[i],C[i] )
        and_list.append(out_bool[i]== Or(And(Not(a),Not(b),c),And(a,Not(b),Not(c)),And(a,b,c),And(Not(a),b,Not(c))))
        and_list.append(C[i-1] == Or(And(a,b),And(a,c),And(b,c)))
    
    return And(and_list)


# def _subtract_bool(a,b):
#     return ( Xor(a,b), Or(Not(a),b) )

# def subtract_bool(A,B):
#     out_bool = BoolVector("o",bit_per_number)
#     and_list = list()
#     for i in reversed(range(bit_per_number)):
#         if i == bit_per_number-1:
#             (diff, borr ) = _subtract_bool(A[i],B[i])
#             and_list.append(out_bool[i] == diff)
#             prev_borr = borr
#         else:
#             (diff_1,borr_1) = _subtract_bool(prev_borr,A[i])
#             (final_diff,final_borr) = _subtract_bool(diff_1,B[i])
#             prev_borr = final_borr
#             #diff without borrow
#             (diff_wo_bor,borr_wo_borr) = _subtract_bool(A[i],B[i])
            
#             and_list.append(out_bool[i] == If(prev_borr==False,final_diff,diff_wo_bor))
#      return And(and_list)

BOUNDARIES = And(
    [
        And([And([
            bool_greateq(X[i],0),
            bool_lesseq(X[i],WB[i])
            ]),
            And([
                bool_greateq(Y[i],0),
                bool_greateq(Y[i],HB[i])
            ]) ]) for i in range(N)] )

solve(add_bool(10,10))