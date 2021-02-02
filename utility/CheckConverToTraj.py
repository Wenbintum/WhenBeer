from ase import Atoms, Atom
from ase.visualize import view
from numpy import array
from ase.io import Trajectory, read, write
from ase.calculators.singlepoint import SinglePointCalculator
from glob import glob
from ase.units import Ry, Bohr
import os 
from ase.constraints import FixAtoms

path = '/p/project/tmosdes/wenxu/graph/Cu/Cu_warehause/Cu_211_filter/'
folder_list = os.listdir(path)
for folder in folder_list:
       with open(f'{path}{folder}/relax.log', 'r') as infile:
           lines = infile.readlines()
       if not float(lines[-1].split()[-1]) <= 0.05:
           print(f'{folder} > 0.05')







