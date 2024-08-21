cwd=$(pwd)
input_path=$(realpath "$2")
output_path=$(realpath "$3")
cd $1
conda_env_path=$(dirname $(dirname "$python_path"))
$conda_env_path/bin/qupkake file $input_path -s input -o intermediate_output.sdf
python code/postprocess.py data/output/intermediate_output.sdf $output_path
rm -rf data
cd $cwd
