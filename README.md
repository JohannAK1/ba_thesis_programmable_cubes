# Bachelor Thesis Programmable Cubes
This project implements the rule-based reconfiguration algorithms proposed in the thesis. The main components are: 
- IPASolver → In-Place Algorithm
- CSASolver → Common Shape Algorithm 
- Generator → Creates Problem Instances (Initial Configuration, Target Configuration, Initial Types and Target Types)
- Programmable Cubes Framework → Challenge Instances and Pivoting Cube Model logic 
- Animation → Creates GIFs of the reconfiguration process 

## How to Run 
The code runs on Python 3.9. To use the proposed algorithms, install the following Python modules: 
````
numba
numpy
matplotlib
````
To test if everything works correctly:

Linux and Mac: 
````
python3 Main.py
````
Windows: 
````
python Main.py
````
This test runs both algorithms to solve the ISS instance of the Programmable Cubes Challenge and generates to GIFs to visualize the reconfiguration process. A simple overview of the algorithms is provided below. 

## In-Place Algorithm (IPA)

**Features:**
- Direct Reconfiguration Algorithm
- Can generate much shorter reconfiguration sequences
- Optimized for efficiency, but is not always able to reconfigure completely

**Visualization:**  
<img src="example_reconfigurations/IPA.gif" width="500" height="500">

## Common Shape Algorithm (CSA)

**Features:**
- Intermediate Configuration Approach
- More robust solution strategy
- Uses intermediate configurations
- Requires more reconfiguration steps

**Visualization:**  
<img src="example_reconfigurations/CSA.gif" width="500" height="500">