#!/usr/bin/env python

from  ase.io import read, write
import os,sys


def read_data(output_name):
    with open('{}'.format(output_name),'r') as input_file:
         lines=input_file.readlines()
         if len(lines) < 1:
            line=0
         else:
            line =lines[-1].split()
         return line

init_dir=os.getcwd()
folnames=os.listdir(init_dir)
folnames.sort()
for folname in folnames:
    os.chdir(folname)
    state = None
    if os.path.exists('relax.log'):
       line=read_data('relax.log')
       if line==0:
           state='SCF failed'
       else:
           if float(line[-1]) <= 0.05:
               state='Conver success'
           else:
               state='Force failed'
    if state == 'SCF failed' or state == 'Force failed':
        os.system('cp /p/project/tmosdes/wenxu/scripts/will_package/utility/re_opt.py .')
        os.system('cp /p/project/tmosdes/wenxu/scripts/will_package/utility/resub_job .')
        os.system('sed -i "s/NAME/\'{}\'/g" re_opt.py'.format(folname+'.traj'))
        os.system('sbatch --job-name=$(basename $PWD) resub_job')
        print('submit {}'.format(folname))
    if state == 'Conver success':
        print('NOT sub {}'.format(folname))
    os.chdir(init_dir)
    



