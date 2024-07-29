# imports
import os
import csv
import sys
from cli import main_file

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



# Create a class to mimic the argument structure expected by main_file
class Args:
    def __init__(self, filename, smiles_col, name_col, root, output, multiprocessing=False, tautomerize=False):
        self.filename = filename
        self.smiles_col = smiles_col
        self.name_col = name_col
        self.root = root
        self.output = output
        self.multiprocessing = multiprocessing
        self.tautomerize = tautomerize



# Set up arguments for batch processing
args = Args(filename=tmp_input_file, smiles_col="smile", name_col="molecule", root=root, output=output_file, tautomerize=False)

# RUN QUPKAKE
main_file(args)

# CLEAN UP TEMPORARY FILE
os.remove(tmp_input_file)
