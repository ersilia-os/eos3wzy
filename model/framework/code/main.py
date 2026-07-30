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
names = ['mol' + str(i) for i in range(len(smiles_list))]

n_cores = max(1, (os.cpu_count() or 2) - 1)

cli_script = os.path.join(root, "qupkake_code", "cli.py")
python_exec = sys.executable

BATCH_SIZES = [1000, 100, 10, 1]


def run_qupkake(smiles_chunk, names_chunk):
    """Run the QUpKAke CLI on a single chunk. Returns counts_data on success, None on failure."""
    chunk_folder = tempfile.mkdtemp(prefix='pkatmp-chunk-', dir=temp_folder)
    chunk_df = pd.DataFrame({"smiles": smiles_chunk, "name": names_chunk})
    chunk_input = os.path.join(chunk_folder, "input.csv")
    chunk_df.to_csv(chunk_input, index=False)

    args = [
        "file",
        chunk_input,
        "--root", chunk_folder,
        "-s", "smiles",
        "-n", "name",
        "-o", "intermediate_output.sdf",
    ]
    if len(smiles_chunk) > 100 and n_cores > 1:
        args += ["-mp", str(n_cores)]

    command = [python_exec, cli_script] + args
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        shutil.rmtree(chunk_folder, ignore_errors=True)
        return None

    chunk_output = extract_pka_from_sdf(names_chunk, os.path.join(chunk_folder, "output", "intermediate_output.sdf"))
    shutil.rmtree(chunk_folder, ignore_errors=True)
    return chunk_output


def run_with_fallback(smiles_chunk, names_chunk, batch_sizes):
    """Try running a chunk as-is; on failure, split it into smaller batches (per batch_sizes cascade).

    Molecules that still fail at the finest granularity (single molecule) get an empty (NaN-like) result.
    """
    size = batch_sizes[0]
    is_last_level = len(batch_sizes) == 1

    if len(smiles_chunk) <= size:
        chunk_output = run_qupkake(smiles_chunk, names_chunk)
        if chunk_output is not None:
            return chunk_output
        if is_last_level:
            return [{} for _ in names_chunk]
        return run_with_fallback(smiles_chunk, names_chunk, batch_sizes[1:])

    results = []
    for i in range(0, len(smiles_chunk), size):
        sub_smiles = smiles_chunk[i:i + size]
        sub_names = names_chunk[i:i + size]
        sub_output = run_qupkake(sub_smiles, sub_names)
        if sub_output is not None:
            results.extend(sub_output)
        elif is_last_level:
            results.extend([{} for _ in sub_names])
        else:
            results.extend(run_with_fallback(sub_smiles, sub_names, batch_sizes[1:]))
    return results


output = run_with_fallback(smiles_list, names, BATCH_SIZES)

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