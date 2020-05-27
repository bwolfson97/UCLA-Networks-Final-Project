# UCLA-Networks-Final-Project

UCLA Networks Final Project is the code for our final project for the UCLA Math 168 Networks class.

## Installation

Use the environment manager [Anaconda](https://www.anaconda.com/products/individual) to build the environment for this project from the `environment.yml` file.

Clone git repo and then use:
```bash
conda env create -f environment.yml
```
to create the environemnt.

## File Overview
`simulation_end_to_end.ipynb`: a jupyter notebook allowing one to set network and simulation parameters and run the simulation end-to-end, producing a final plot of S, I, R, and D(eaths) over time.

`end_to_end.py`: module containing function to run entire end_to_end pipeline, i.e. run simulation **and** analyze results.

`simulation.py`: module containing functions to run simulation loop.

`analysis.py`: module containing functions to analyze and plot simulation data.

## License
[MIT](https://choosealicense.com/licenses/mit/)
