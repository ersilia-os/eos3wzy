# imports
import os
import csv
import sys
from cli import parse_arguments, extract_pka_statistics_from_sdf


# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)


# INPUT ADAPTER FUNCTION
# function reads the single-column CSV file, 
# converts it to the two-column format, 
# and writes it to a temporary file (tmp_input.csv).
def convert_input_file(input_file, tmp_file):

    smiles_list = []

    # read single column CSV file 
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for r in reader:
            smiles_list.append(r[0])

    # write input into temprary file
    with open(tmp_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["molecule", "smile"])  # header
        for i, smi in enumerate(smiles_list):
            writer.writerow([f"mol{i}", smi])
    
    return tmp_file


# CONVERT INPUT FILE INTO THE REQUIRED FORMAT
tmp_input_file = os.path.join(root, "tmp_input.csv")
convert_input_file(input_file, tmp_input_file)


# RUN QUPKAKE
# Create a list of arguments as if they were passed from the command line
qupkake_args = ["file", tmp_input_file, "-o", "qupkake_output.sdf"]

# Parse the arguments
parsed_args = parse_arguments(qupkake_args)

# Construct the full paths for the SDF and CSV files
base_dir = os.getcwd()
sdf_file = os.path.join(base_dir, 'data/output/qupkake_output.sdf')
csv_file = os.path.join(base_dir, 'data/output/predicted_pKa_values.csv')

# Check if the SDF file was created successfully (if protonation/deprotonation site was found)
if not os.path.exists(sdf_file):
    extract_pka_statistics_from_sdf(sdf_file, csv_file, no_protonation=True)
    sys.exit(1)

# Convert the SDF file to CSV
extract_pka_statistics_from_sdf(sdf_file, csv_file, no_protonation=False)

# Remove the intermediate SDF file
if os.path.exists(sdf_file):
    os.remove(sdf_file)

# CLEAN UP TEMPORARY FILE
os.remove(tmp_input_file)
