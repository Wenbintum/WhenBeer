from itertools import combinations
from itertools import permutations
from ase import Atoms, Atom
import numpy as np
from ase.io import read,write
from ase.build import add_adsorbate,molecule
#root
from parameter import surface_index 

def  graphene_cell (supercell):
        ######build graphene cell
        deg60 = 60*np.pi/180

        halfsqrt3 = np.sqrt(3) / 2.

        atoms = Atoms('C2', positions = [[0,0,0], [ 1.42, 0, 0]])

        atoms.set_cell(np.sqrt(3) * 1.42 * np.array([[halfsqrt3, 0.5, 0], [halfsqrt3, -0.5 ,0.], [0,0,0]]))

        atoms.center(axis=2, vacuum=10.)
        atoms=atoms*(supercell,supercell,1)
        return atoms

def build_2H_2O_graphene():
        atoms_list=[]
        index_list =[]
        list_ortho= [30,31]
        list_para  = [29,42]
        ##This yields  2*H and 2*O  index in ortho and para.   para=down + right. ortho=up + right
        name_list=surface_index.index.keys()
        for name in name_list:
            list_init  =list(combinations(surface_index.index[name],2))
            list_repeat=list(combinations(surface_index.repeat_index[name],2))
            for i in list_repeat:
                list_init.remove(i)
            for  k in range(len(list_init)):
                supercell=6
                atoms = graphene_cell(supercell)
                if name[:4] == 'orth':
                    list_add= list_ortho + list(list_init[k])
                if name[:4] == 'para':
                    list_add= list_para + list(list_init[k])
                add_adsorbate(atoms,'H',1,     (atoms[list_add[0]].position[0],atoms[list_add[0]].position[1]))
                add_adsorbate(atoms,'H',1,     (atoms[list_add[1]].position[0],atoms[list_add[1]].position[1]))
                add_adsorbate(atoms,'O',1.2, (atoms[list_add[2]].position[0],atoms[list_add[2]].position[1]))
                add_adsorbate(atoms,'O',1.2, (atoms[list_add[3]].position[0],atoms[list_add[3]].position[1]))
                
                atoms_list.append(atoms)
                index_list.append(list_add)
        return atoms_list, index_list

def Getlength(atoms,p1,p2):
    x1,y1=atoms[p1].position[0], atoms[p1].position[1]
    x2,y2=atoms[p2].position[0], atoms[p2].position[1]
    length = ((x1-x2)**2+(y1-y2)**2)**0.5
    return length
def Area_triangle(atoms,p1,p2,p3):
    l1= Getlength(atoms,p1,p2)
    l2= Getlength(atoms,p2,p3)
    l3= Getlength(atoms,p1,p3)
    s=(l1+l2+l3)/2
    area = (s*(s-l1)*(s-l2)*(s-l3))**0.5
    return area
def build_H_O_OH():
    supercell=6
    atoms = graphene_cell(supercell)
    
    co_3_list=list(combinations(surface_index.co_3_ads,3))
    #list1 with area
    co_3_area_collect=[]
    for co_3 in co_3_list:
        co_3_area_collect.append(round(Area_triangle(atoms,co_3[0],co_3[1],co_3[2]),4))
    #list 2 with no repeating area
    #list 3 with index of no repeating area
    co_3_norepeat=[]
    co_3_index=[]
    for n, k in enumerate(co_3_area_collect,0):
            if k not in co_3_norepeat:
                co_3_norepeat.append(k)
                co_3_index.append(n)
    # print co_3_index
    # print co_3_norepeat
    co_3_collect=[]
    atoms_list=[]
    index_list=[]
    for index in co_3_index:
        for i in list(permutations(co_3_list[index],3)):
            co_3_collect.append(i)
    mol_OH=Atoms('OH',[(0,0,0),(-np.cos(np.pi/4)*0.979,0,np.sin(np.pi/4)*0.979)])
    for k in range(len(co_3_collect)):
        supercell=6
        atoms = graphene_cell(supercell)

        add_adsorbate(atoms,'H',1,       (atoms[co_3_collect[k][0]].position[0],atoms[co_3_collect[k][0]].position[1]))
        add_adsorbate(atoms,'O',1.2,     (atoms[co_3_collect[k][1]].position[0],atoms[co_3_collect[k][1]].position[1]))
        add_adsorbate(atoms,mol_OH,1.3,  (atoms[co_3_collect[k][2]].position[0],atoms[co_3_collect[k][2]].position[1]))
        atoms_list.append(atoms)
	index_list.append(co_3_collect[k])
    return atoms_list,index_list

def build_H_OOH():
    mol=Atoms('OOH',[(0,0,-1.25),(0,0,0),(-np.cos(np.pi/4)*0.979,0,np.sin(np.pi/4)*0.979)])
    atoms_list=[]
    index_list=[]
    for k in range(len(surface_index.co_2_ads)):
        supercell=6
        atoms = graphene_cell(supercell)
        add_adsorbate(atoms,'H',1,   (atoms[surface_index.co_2_ads[k][0]].position[0],atoms[surface_index.co_2_ads[k][0]].position[1]))
        add_adsorbate(atoms,mol,1.5, (atoms[surface_index.co_2_ads[k][1]].position[0],atoms[surface_index.co_2_ads[k][1]].position[1]))
        atoms_list.append(atoms)
        index_list.append(surface_index.co_2_ads[k])
    return atoms_list,index_list
 
if __name__ == "__main__":
    
    atoms_list, index_list =build_2H_2O_graphene()
    atoms_list[30].edit()
    for i in index_list:
	print i
    
