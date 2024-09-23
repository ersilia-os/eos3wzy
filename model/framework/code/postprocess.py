import os
import sys
import pandas as pd
from rdkit import Chem

def extract_pka_statistics_from_sdf(sdf_file):
    """
    Extracts pKa statistics from an SDF file and writes them to a CSV file.

    Parameters
    ----------
    sdf_file : str
        Path to the input SDF file containing pKa predictions.
    csv_file : str
        Path to the output CSV file where the statistics will be stored.
    """
    summary_data = {}

    # Check if the SDF file exists
    if not os.path.exists(sdf_file):
        print(f"Error: SDF file '{sdf_file}' not found.")
        return None

    # Read the SDF file using RDKit
    supplier = Chem.SDMolSupplier(sdf_file)
    if not supplier:
        print(f"Error: Failed to read SDF file '{sdf_file}'.")
        sys.exit(1)

    # Process each molecule in the SDF file
    for mol in supplier:
        name = mol.GetProp("_Name")
        if name not in summary_data:
            summary_data[name] = []
        print(name)
        if mol is None:
            continue
        pka = mol.GetProp('pka')
        pka = float(pka)
        idx = mol.GetProp("idx")
        pka_type = mol.GetProp("pka_type")
        summary_data[name].append(pka)

    return summary_data
