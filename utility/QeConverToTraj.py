from ase import Atoms, Atom
from ase.visualize import view
from numpy import array
from ase.io import Trajectory, read, write
from ase.calculators.singlepoint import SinglePointCalculator
from glob import glob
from ase.units import Ry, Bohr
import os 
from ase.constraints import FixAtoms

path = '/p/project/tmosdes/wenxu/graph/Cu/Cu_211/'
copy_path = '/p/project/tmosdes/wenxu/graph/Cu/Cu_warehause/'
folder_list = os.listdir(path)
for folder in folder_list:
    files = os.listdir(path + folder)
    for file in files:
        if file.startswith('esp'):
           espname = file #this will choose esp_numer with large number
    try:
        with open(f'{path}{folder}/{espname}/log', 'r') as infile:
            lines = infile.readlines()
    except:
            print(f'log file does not exist for {folder}')
            continue
    atoms = Atoms(None)
    converged = False

    nline = 0
    for line in lines:
        if 'celldm(1)=' in line:
           factor = float(line[17:26])*Bohr
        elif 'a(1) = (' in line:
           a1 = line[23:57]
        elif 'a(2) = (' in line:
           a2 = line[23:57]
        elif 'a(3) = (' in line:
           a3 = line[23:57]
        elif '!    total energy' in line:
           e = float(line[32:49])
        elif '     smearing contrib. (-TS)' in line:
           eTS = float(line[32:49])
        elif 'bfgs converged in ' in line:
           converged = True
        elif 'Begin final coordinates' in line:
           coord_start = nline + 3
        elif 'End final coordinates' in line:
           coord_end = nline
        nline += 1

    if converged:

       a1x,a1y,a1z = [float(x)*factor for x in list(filter(lambda a: a != '', a1.strip().split(' ')))]
       a2x,a2y,a2z = [float(x)*factor for x in list(filter(lambda a: a != '', a2.strip().split(' ')))]
       a3x,a3y,a3z = [float(x)*factor for x in list(filter(lambda a: a != '', a3.strip().split(' ')))]
       cell = [[a1x,a1y,a1z], [a2x,a2y,a2z], [a3x,a3y,a3z]]
      # print(cell)
       atoms.set_cell(cell)
       fix_index = []
       for i,line in enumerate(lines[coord_start:coord_end]):                                                                                                                
           values = list(filter(lambda a: a not in [''], line.strip().split(' ')))                                                                                           
           if values[-1] == '0' and values[-2] =='0' and values[-3]=='0':                                                                                                    
              fix_index.append(i)   
           element = values[0][:-1]
           xpos = float(values[1])
           ypos = float(values[2])
           zpos = float(values[3])
           pos = array([a1x,a1y,a1z])*xpos + array([a2x,a2y,a2z])*ypos + array([a3x,a3y,a3z])*zpos
           #print(element, pos)
           atoms.append(Atom(element,pos))
       atoms.pbc = True
       c = FixAtoms(indices=fix_index)
       atoms.set_constraint(c)

       with open(f'{path}{folder}/relax.log', 'r') as infile:
           lines = infile.readlines()
       if not float(lines[-1].split()[-1]) <= 0.05:
           print(f'{folder} > 0.05')
           if not os.path.exists(path+'wrong_force/'+folder):
                  os.system(f'mv {path}{folder} {path}wrong_force')
       else:
           total_energy = float(lines[-1].split()[-2])
           calc = SinglePointCalculator(atoms, energy=total_energy)
           atoms.set_calculator(calc)
           write(f'{path}{folder}/opt_ase.traj', atoms)
           
           os.system(f'mkdir {copy_path}{folder}')
           os.system(f'cp {path}{folder}/{folder}.traj {copy_path}{folder}/{folder}.traj')
           os.system(f'cp {path}{folder}/opt_ase.traj  {copy_path}{folder}/opt_ase.traj')
           os.system(f'cp {path}{folder}/relax.log     {copy_path}{folder}/relax.log')
    else:
       print(f'BFGS not converged for {folder}')







