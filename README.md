# Predict micro-pKa of organic molecules

QupKake is an innovative approach that combines graph neural network (GNN) models with semiempirical quantum mechanical (QM) features to forecast the micro-pKa values of organic molecules. QM has a significant role in both identifying reaction sites and predicting micro-pKa values. Precisely predicting micro-pKa values is vital for comprehending and adjusting the acidity and basicity of organic compounds. This has significant applications in drug discovery, materials science, and environmental chemistry.

This model was incorporated on 2024-07-17.Last packaged on 2025-11-21.

## Information
### Identifiers
- **Ersilia Identifier:** `eos3wzy`
- **Slug:** `qupkake`

### Domain
- **Task:** `Annotation`
- **Subtask:** `Property calculation or prediction`
- **Biomedical Area:** `Any`
- **Target Organism:** `Any`
- **Tags:** `pKa`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `22`
- **Output Consistency:** `Fixed`
- **Interpretation:** An array of 22 dimensions is given, counting the number of atoms with an acidic or basic pKa value rounded at 0, 1, 2, 3... up to 10.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| pka_acidic_0 | integer | high | Atoms with predicted acidic pKa close to 0 |
| pka_acidic_1 | integer | high | Atoms with predicted acidic pKa close to 1 |
| pka_acidic_2 | integer | high | Atoms with predicted acidic pKa close to 2 |
| pka_acidic_3 | integer | high | Atoms with predicted acidic pKa close to 3 |
| pka_acidic_4 | integer | high | Atoms with predicted acidic pKa close to 4 |
| pka_acidic_5 | integer | high | Atoms with predicted acidic pKa close to 5 |
| pka_acidic_6 | integer | high | Atoms with predicted acidic pKa close to 6 |
| pka_acidic_7 | integer | high | Atoms with predicted acidic pKa close to 7 |
| pka_acidic_8 | integer | high | Atoms with predicted acidic pKa close to 8 |
| pka_acidic_9 | integer | high | Atoms with predicted acidic pKa close to 9 |

_10 of 22 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos3wzy](https://hub.docker.com/r/ersiliaos/eos3wzy)
- **Docker Architecture:** `AMD64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos3wzy.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos3wzy.zip)

### Resource Consumption
- **Model Size (Mb):** `222`
- **Environment Size (Mb):** `4730`
- **Image Size (Mb):** `6562.62`

**Computational Performance (seconds):**
- 10 inputs: `37.13`
- 100 inputs: `-1`
- 10000 inputs: `-1`

### References
- **Source Code**: [https://github.com/hutchisonlab/QupKake](https://github.com/hutchisonlab/QupKake)
- **Publication**: [https://doi.org/10.1021/acs.jctc.4c00328](https://doi.org/10.1021/acs.jctc.4c00328)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2024`
- **Ersilia Contributor:** [LauraGomezjurado](https://github.com/LauraGomezjurado)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [BSD-3-Clause](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos3wzy
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos3wzy
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
