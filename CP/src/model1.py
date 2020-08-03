import argparse
import sys
from minizinc import Instance, Model, Solver
from pathlib import Path

parser = argparse.ArgumentParser(description="Minizinc solver in python")
parser.add_argument("--solver",help="Solver to use: (gecode|chuffed)",default="gecode",action="store")
parser.add_argument("--model",help="PATH of the model file (*.mzn)",action="store")
parser.add_argument("--instance",help="PATH of the instances as formatted in the document of the project",action="store")
parser.add_argument("--out_dir",help="DIR where to save the output",default="")

if (len(sys.argv) > 1):
    args = parser.parse_args()
else:
    test_args = ['D:\\University\\PROJECTS\\COP2\\Dicosola - PWP Project\CP\src\\model1.mzn','D:\\University\\PROJECTS\COP2\\Dicosola - PWP Project\\Instances\\9x12-example.txt']
    args = parser.parse_args(["--solver","gecode","--model",test_args[0],"--instance",test_args[1]])

## Read the instance file
# Dictionary that will contains data instance
data = { }
# Init empty list for X and Y
data["widths"] = []
data["heights"] = []

with open(args.instance) as instances_file:
    for index,line in enumerate(instances_file):
        if ((line.strip())):    
            line = line.strip()
            if index == 0:
                data["W"] = int(line.split()[0])
                data["H"] = int(line.split()[1])
            elif index == 1:
                data["N"] = int(line)
            else:
                s = line.split()
                data["widths"].append(int(s[0]))
                data["heights"].append(int(s[1]))

## Prepare the model
solver = Solver.lookup(args.solver)
if args.solver == "gecode":
    solver.stdFlags = ['-p','6'] # use 6 thread
model = Model(args.model)
instance = Instance(solver,model)
# Set the data inside the model
for key in data:
    instance[key] = data[key]


result = instance.solve()
print(result.statistics)
print(result)


filename = Path(args.instance).stem
out_name = f"{filename}-out.txt"
report_name = f"{filename}-{args.solver}-report.txt"

if len(args.out_dir) > 0:
    out_dir = Path(args.out_dir) 
    out_path = out_dir / out_name
    report_path = out_dir / report_name

    with open(out_path,'w') as out_file:
        out_file.write(str(result))
    # with open(report_path,'w') as report_file:
        # report_file.write(str(result.statistics))

