import os
import sys
import numpy as np
import collections
from rdkit import Chem

def extract_pka_from_sdf(molecule_names, sdf_file):
    """
    Extracts pKa statistics from an SDF file and writes them to a CSV file.

    Parameters
    ----------
    sdf_file : str
        Path to the input SDF file containing pKa predictions.
    csv_file : str
        Path to the output CSV file where the statistics will be stored.
    """
    summary_data = collections.defaultdict(list)

    # Check if the SDF file exists
    if not os.path.exists(sdf_file):
        print(f"Error: SDF file '{sdf_file}' not found.")
        return None

    # Read the SDF file using RDKit
    supplier = Chem.SDMolSupplier(sdf_file)
    if not supplier:
        print(f"Error: Failed to read SDF file '{sdf_file}'.")
        return None

    # Process each molecule in the SDF file
    names = []
    for mol in supplier:
        name = mol.GetProp("_Name")
        if name not in summary_data:
            summary_data[name] = []
        names += [name]
        if mol is None:
            continue
        pka = mol.GetProp('pka')
        pka = float(pka)
        idx = int(mol.GetProp('idx'))
        pka_type = mol.GetProp("pka_type")
        summary_data[name] += [(idx, pka_type, pka)]

    counts_data = []
    for name in molecule_names:
        if name not in summary_data:
            counts_data += [{}]
        else:
            data = summary_data[name]
            data_idxs = collections.defaultdict(list)
            for v in data:
                idx, pka_type, pka = v
                data_idxs[(idx, pka_type)] += [pka]
            data_idxs = dict((k, np.mean(v)) for k,v in data_idxs.items())
            counts = collections.defaultdict(int)
            for k, v in data_idxs.items():
                pka_type = k[1]
                vint = int(np.round(v, 0))
                vint = int(np.clip(vint, 0, 10))
                counts[(pka_type, vint)] += 1
            counts_data += [dict(counts)]

    return counts_data
