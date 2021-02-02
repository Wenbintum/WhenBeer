#!/usr/bin/env python
from sys import path
import os, sys
from ase import Atom,Atoms
from espresso import Espresso, iEspresso
from ase.optimize import BFGS
import numpy as np
from ase.io import read,write
from ase.units import Rydberg, Bohr
#root
atoms=read(NAME)

symbols = [atom.symbol for atom in atoms]
if 'Fe' in symbols or 'Co' in symbols or 'Ni' in symbols:
    spin_pol = True
else:
    spin_pol = False

if  'Cu' in symbols:
    econv = 0.000001
elif 'Ni' in symbols or 'Fe' in symbols or 'Co' in symbols:
    econv = 0.0005
else:
    econv = 0.000005

convergence = {'energy':econv,
               'mixing':0.1,
               'nmix':10,
               'maxsteps':500,
               'diag':'david'
                }

dipole = {'status':True}

output = {'avoidio':False,
          'removewf':True,
          'wf_collect':False}

calc =  Espresso(pw= 500, #* Rydberg,
                 dw = 5000, #* Rydberg
                 beefensemble=True,
                 kpts = (4, 4, 1),
                 nbands = -15,
                 xc = 'BEEF-vdw',
                 sigma = 0.1,
                 convergence = convergence,
                 dipole = dipole,
                 spinpol=spin_pol,
                 outdir = 'esp.log',
                 ion_dynamics='bfgs',
                 nstep = 200,
                 output = output,
                 psppath='/p/project/tmosdes/wenxu/code_new/db_pp'
                 )
atoms.set_calculator(calc)
qn = BFGS(atoms, logfile='relax.log',trajectory='opt.traj')
qn.run(fmax=0.05)
