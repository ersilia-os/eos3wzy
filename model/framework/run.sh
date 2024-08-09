cwd=$(pwd)
cd $1
qupkake file $2 -s smiles -o intermediate_output.sdf
python code/postprocess.py data/outputs/intermediate_output.sdf $3
rm -rf data
cd $cwd
