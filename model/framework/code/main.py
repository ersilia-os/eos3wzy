# imports
import os
import csv
import sys
import tempfile
import subprocess
import shutil
import pandas as pd

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)

from qupkake_code.cli import main
from postprocess import extract_pka_statistics_from_sdf

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

temp_folder = tempfile.mkdtemp(prefix='ersilia_')

# read SMILES from .csv file, assuming one column with header
with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)
    smiles_list = [r[0] for r in reader]

#the name is needed to process multiple molecules
df = pd.read_csv(input_file)
names = ['mol' + str(i) for i in range(len(df))]
df['name'] = names
input_with_name = os.path.join(temp_folder, "input.csv")
df.to_csv(input_with_name, index=False)

cli_script = os.path.join(root,"qupkake_code", "cli.py")
args = [
    "file",
    input_with_name,
    "--root", temp_folder,
    "-s", "input",
    "-n", "name",
    "-o", "intermediate_output.sdf"
]

python_exec = sys.executable
command = [python_exec, cli_script] + args
subprocess.run(command)

output = extract_pka_statistics_from_sdf(os.path.join(temp_folder, "output/intermediate_output.sdf"))


R = []

for n in names:
    if output is None:
        r = [None]*10
    else:
        if n in output:
            r = sorted(output[n])
            if len(r) > 10:
                r = r[:5] + r[5:]
            if len(r) < 10:
                r = r + [None]*(10-len(r))
        else:
            r = [None]*10
    R += [r]

header = ["pka_{0}".format(i) for i in range(10)]

shutil.rmtree(temp_folder)
# write output in a .csv file
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)  # header
    for r in R:
        writer.writerow(r)