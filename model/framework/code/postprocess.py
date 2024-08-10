import os
import sys
import pandas as pd
from rdkit import Chem

def extract_pka_statistics_from_sdf(sdf_file, csv_file):
    """
    Extracts pKa statistics from an SDF file and writes them to a CSV file.

    Parameters
    ----------
    sdf_file : str
        Path to the input SDF file containing pKa predictions.
    csv_file : str
        Path to the output CSV file where the statistics will be stored.
    """
    summary_data = []

    # Check if the SDF file exists
    if not os.path.exists(sdf_file):
        print(f"Error: SDF file '{sdf_file}' not found.")
        sys.exit(1)

    # Read the SDF file using RDKit
    supplier = Chem.SDMolSupplier(sdf_file)
    if not supplier:
        print(f"Error: Failed to read SDF file '{sdf_file}'.")
        sys.exit(1)

    # Process each molecule in the SDF file
    for mol in supplier:
        if mol is None:
            continue
        
        mol_name = mol.GetProp('_Name') if mol.HasProp('_Name') else 'Unknown'

        if mol.HasProp('pka'):
            pka_list = mol.GetProp('pka').split(',')
            pkas = [float(pka.strip('tensor()')) for pka in pka_list]

            min_pka = min(pkas)
            avg_pka = sum(pkas) / len(pkas)
            max_pka = max(pkas)
            num_pkas = len(pkas)

            summary_data.append({
                'Molecule': mol_name,
                'min_pka': min_pka,
                'avg_pka': avg_pka,
                'max_pka': max_pka,
                'num_pkas': num_pkas
            })

    # Convert the summary data to a pandas DataFrame and save it as a CSV file
    df = pd.DataFrame(summary_data)
    df.to_csv(csv_file, index=False)
    print(f"pKa statistics saved to {csv_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python postprocess.py <input_sdf_file> <output_csv_file>")
        sys.exit(1)

    sdf_file = sys.argv[1]
    csv_file = sys.argv[2]

    extract_pka_statistics_from_sdf(sdf_file, csv_file)
