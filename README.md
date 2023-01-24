# Modelling the Ecosystem of Rossumøya

---

The project simulates life at the imaginary island of Rossumøya, given several initial parameters.
As a user and initializer you have the possibility to create an island of your choice with pre-
defined values for the different parameters. Another option is to run simulations with the default
set of parameters. In the examples folder you are presented with some examples of different types
of simulations. What varies is the size of the island, the distribution of landscape types, and 
the distribution and initialization of animals. 

### How the simulation works
Defining the geography of the island:
```
geogr = """\
           WWWW
           WLHW
           WWWW"""
```
Border can only be water, everything else can be either **Highland(H)**, **Lowland(L)**, or 
**Desert(D)**.

Initiating the population of the island:
```
ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]
    ini_carns = [{'loc': (2, 3),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(20)]}]
```
Choose the location, species and their age and weight. The rest of the parameters are taken from the 
default values, but can be changed and specified by the user (see example 3).

Initializing the simulation:
```
for seed in range(100, 103):
    sim = BioSim(geogr, [ini_herbs and/or ini_herbs], seed=seed,
                 log_file=f'data/simulation_hc_{seed:05d}',
                 img_dir='data', img_base=f'simulation_hc_{seed:05d}', img_years=300)
```

The different parameters and what type of values that can be used is documented
[here](src/biosim/simulation.py) in ```biosim/simulation.py```.

The final simulation is called by using```sim.simulate(301)```, defining number of years to
simulate.

Where the chosen value is the number of years you want to simulate. For further documentation and 
information about the different classes, parameters and possible restrictions is documented in each
file and package in the folder ```biosim```, [here](src/biosim).

---

## Examples of simulations

#### 1. Simulation with a default set of parameters
```
examples/simulation_migration_default_params.py
``` 
[Python file here](examples/simulation_migration_default_params.py).
Simulation of 10 years with only Herbivores, then Carnivores are added and the simulation goes on
for 50 more years. Weight and age of animals are initialized, and the number of each fauna type.
Default parameters used. Map and distribution of animals is shown in console, and statistics are 
visualized in a separate window. Showing 59 years in total.
#### 2. Simulation with changed parameters
```
examples/simulation_hc_changed_params.py
```
[Python file here](examples/simulation_hc_changed_params.py)
Simulation of 10 years with only Herbivores, then Carnivores are added and the simulation goes on
for 251 more years (260 years in total). Some of the parameters have been changed.

#### 3. Full simulation with visualization over 200 years
```
examples/simulation.visual.py
```
[Python file here](examples/simulation_visual.py), we simulate a period of 400 years. 
The initialized animals in year 0 are 200 Herbivores and 50 Carnivores. The movie found 
[here](Exam/simulation_visual.mp4) is the changes visualized per year from this simulation. 




### Extra additions
#### 1. 
In ```biosim/simulation.py```, an extra parameter has been added to the *BioSim*-class parameters: 
**console_output_island**. Setting this to *True* enables print-out of island map in the console. 
Running ```examples/simulation.py``` ([here](examples/simulation_migration.py)) gives us the following output in the console for year 3:
![Output of island map in console.](readme_imgs/console_map.png)
The parameters in the mentioned file is set in a way so that we can observe that the migration 
for each animal in each cell works properly (following the set restrictions).

#### 2. 
The image below presents how the statistics from the simulation are visualized. In the two windows
showing the distribution of Herbivore and Carnivores, we have chosen to make the part of the map 
that is set to geography type *Water*, blue. 
The distribution is set by getting the details of the animals in each cell, and we then set the 
length of the animals to be equal 1. While refreshing the heatmaps we set a mask on the cells where 
the number of animals is equal to -1 (which is done where there is geo type water on the map). 
In visuals.py, [here](src/biosim/visualization/visuals.py), the color of this mask is set to blue.
This ensures that the water areas are masked, and therefore blue, making the visualization better.
![Output of island map in separate window](readme_imgs/stats_visual.png)

  
#### 3. 
-- added str to make debugging easier --
-- take pictures of different types of debugging --

### Credits:
 - Code optimization done with Sourcery: https://sourcery.ai/


### Authors and contributors to the project
- Sougata Bhattacharya, sougata.bhattacharya@nmbu.no
- Tonje Martine Lorgen Kirkholt, tonje.martine.lorgen.kirkholt@nmbu.no

[![Pipeline Status](https://gitlab.com/nmbu.no/emner/inf200/h2022/january-block-teams/a39_sougata_tonje/biosim-a39-sougata-tonje/badges/main/pipeline.svg)](https://gitlab.com/nmbu.no/emner/inf200/h2022/january-block-teams/a39_sougata_tonje/biosim-a39-sougata-tonje/-/pipelines?page=1&scope=branches&ref=main)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Flake8 badge](https://img.shields.io/badge/linting-flake8-blue)](https://flake8.pycqa.org/en/latest/)  
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)  
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  
[![made-with-sphinx-doc](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/)   
[![Tox badge](https://img.shields.io/badge/Made%20with-tox-yellowgreen)](https://tox.wiki/en/latest/)