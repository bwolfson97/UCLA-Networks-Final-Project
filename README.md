# UCLA-Networks-Final-Project

UCLA Networks Final Project is the code for our final project for the UCLA Math 168 Networks class. Read our final report [here](modeling_covid.pdf). Note, the final report was written in the style of the journal PNAS, but it was not actually submitted to PNAS.

## Installation

Use the environment manager [Anaconda](https://www.anaconda.com/products/individual) to build the environment for this project from the `environment.yml` file.

Clone git repo and then use:
```bash
conda env create -f environment.yml
```
to create the environemnt.

## File Overview
`experiments.ipynb`: a jupyter notebook running experiments on the effects of inmate release interventions and stopping inmate inflow interventions on the spread of coronavirus in prisons. The output of these experiments may be found in the `experiments.html` and `experiments.pdf` files (both files contain same information).

`end_to_end.py`: module containing function to run entire end_to_end pipeline, i.e. run simulation **and** analyze results.

`simulation.py`: module containing functions to run simulation loop.

`analysis.py`: module containing functions to analyze and plot simulation data.

`tests.py`: script that tests that various aspects of the simulation are working properly.

## License
[MIT](https://choosealicense.com/licenses/mit/)
