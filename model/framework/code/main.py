# imports
import os
import csv
import sys
import tempfile
import subprocess
import shutil
import pandas as pd
from rdkit import Chem

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)

from postprocess import extract_pka_from_sdf

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

temp_folder = tempfile.mkdtemp(prefix='pkatmp-')

# read SMILES from .csv file, assuming one column with header
with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)
    smiles_list = [r[0] for r in reader]

N = len(smiles_list)

keep_idxs = []
smiles_list_ = []
for i, smiles in enumerate(smiles_list):
    try:
        mol = Chem.MolFromSmiles(smiles)
    except:
        mol = None
    if mol is None:
        continue
    keep_idxs += [i]
    smiles_list_ += [smiles]
smiles_list = smiles_list_[:]

#the name is needed to process multiple molecules
df = pd.DataFrame(smiles_list, columns=["smiles"])
names = ['mol' + str(i) for i in range(len(df))]
df['name'] = names
input_with_name = os.path.join(temp_folder, "input.csv")
df.to_csv(input_with_name, index=False)

n_cores = max(1, (os.cpu_count() or 2) - 1)

cli_script = os.path.join(root,"qupkake_code", "cli.py")
args = [
    "file",
    input_with_name,
    "--root", temp_folder,
    "-s", "smiles",
    "-n", "name",
    "-o", "intermediate_output.sdf",
]

if len(smiles_list) > 100 and n_cores > 1:
    args += ["-mp", str(n_cores)]

python_exec = sys.executable
command = [python_exec, cli_script] + args
subprocess.run(command)

try:
    output = extract_pka_from_sdf(names, os.path.join(temp_folder, "output/intermediate_output.sdf"))
except Exception:
    output = None
if output is None:
    output = [{} for _ in names]

header = []
for pka_type in ["acidic", "basic"]:
    for i in range(11):
        header += ["pka_{0}_{1}".format(pka_type, i)]

header2idx = {h: i for i, h in enumerate(header)}

R = [['']*len(header) for _ in range(N)]

for i, out in enumerate(output):
    idx = keep_idxs[i]
    if not out:
        R[idx] = [''] * len(header)
    else:
        r = [0] * len(header)
        for k, v in out.items():
            pka_type, vint = k
            header_key = "pka_{0}_{1}".format(pka_type, vint)
            idx_ = header2idx[header_key]
            r[idx_] = v
        R[idx] = r

shutil.rmtree(temp_folder)

# write output in a .csv file
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for r in R:
        writer.writerow(r)