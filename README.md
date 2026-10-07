# Predict micro-pKa of organic molecules

Counts, across 22 bins, how many atoms in a molecule carry an acidic or basic micro-pKa near each integer from 0 to 10, giving a profile of ionisable sites rather than a single value. QupKake, from Abarbanel and Hutchison, first picks candidate reaction sites with a graph neural network, then predicts each site's pKa from GFN2-xTB semi-empirical quantum chemistry features, with transfer learning onto 5,637 compounds carrying measured micro-pKa values. Root-mean-square errors of 0.5 to 0.8 pKa units were reported on five external test sets.

This model was incorporated on 2024-07-17.Last packaged on 2026-07-30.

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
- **Interpretation:** Counts of atoms with acidic or basic micro-pKa values falling in each integer bin from 0 to 10.

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
- **Environment Size (Mb):** `4765`
- **Image Size (Mb):** `5127.99`

**Computational Performance (seconds):**
- 10 inputs: `42.3`
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
