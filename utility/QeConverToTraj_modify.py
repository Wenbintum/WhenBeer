from ase import Atoms, Atom
from ase.visualize import view
from numpy import array
from ase.io import Trajectory
from ase.calculators.singlepoint import SinglePointCalculator
from glob import glob
from ase.units import Ry, Bohr
from ase.io import read, write

dirs = []
calcpath = 'Cu111/graphene/Cu-gr/D3_esp-develop'
dirs+=glob(calcpath)

for d in dirs:
atoms = Atoms(None)
converged = False
try:
    with open('log') as infile:
        lines = infile.readlines()
except:
    print('log file does not exist for %s'%d)
#    continue

#Extract various info
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
       # if d == 'graphene_noASE':
       #     coord_start = nline + 10
       # else:
            coord_start = nline + 3
    elif 'End final coordinates' in line:
        coord_end = nline
    nline += 1
#Force generation of C21 slab
#if d == 'Cu111-D3/C21':
#    coord_start = 35168
#    coord_end = 35333
#    converged = True
if converged:
    #Set cell
    a1x,a1y,a1z = [float(x)*factor for x in list(filter(lambda a: a != '', a1.strip().split(' ')))]
    a2x,a2y,a2z = [float(x)*factor for x in list(filter(lambda a: a != '', a2.strip().split(' ')))]
    a3x,a3y,a3z = [float(x)*factor for x in list(filter(lambda a: a != '', a3.strip().split(' ')))]
    cell = [[a1x,a1y,a1z], [a2x,a2y,a2z], [a3x,a3y,a3z]]
    print(cell)
    atoms.set_cell(cell)
    #Extract elements and coordinates
    for line in lines[coord_start:coord_end]:
        values = list(filter(lambda a: a not in ['','0'], line.strip().split(' ')))
        element = values[0][:-1]
        xpos = float(values[1])
        ypos = float(values[2])
        zpos = float(values[3])
        pos = array([a1x,a1y,a1z])*xpos + array([a2x,a2y,a2z])*ypos + array([a3x,a3y,a3z])*zpos
        #pos = [xpos, ypos, zpos]
        print(element, pos)
        atoms.append(Atom(element,pos))
    atoms.pbc=True
    #atoms.wrap()
    #view(atoms)
    #calc = SinglePointCalculator(atoms, energy=(e+0.5*eTS)*Ry)
    calc = SinglePointCalculator(atoms, energy=e*Ry)
    atoms.set_calculator(calc)
    write('opt_ase.traj', atoms)
    #traj = Trajectory('opt.traj', 'w')
    #traj.write(atoms)
else:
    print('BFGS not converged for %s'%d)

