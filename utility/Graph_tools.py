import os,sys
import ase.io
import networkx as nx
from ase import neighborlist
from networkx.algorithms.isomorphism import is_isomorphic
import matplotlib.pyplot as plt

nm = nx.algorithms.isomorphism.numerical_node_match('number', 1)

def Node_representation(atoms, cutoff_mult=1, skin=0.1):    #adjacency matrix
    cutoff       = neighborlist.natural_cutoffs(atoms,mult=cutoff_mult)
    neighborList = neighborlist.NeighborList(cutoff, self_interaction=False, bothways=True, skin=skin)
    neighborList.update(atoms)
    node_matrix  = neighborList.get_connectivity_matrix(sparse=False).astype(float)
    return node_matrix

def GraphWithNodes(atoms, skin=0.1):
    G = nx.from_numpy_matrix(Node_representation(atoms, cutoff_mult = 1, skin=skin), parallel_edges=True,
        create_using=nx.MultiGraph)
    nodes = [[i, {'number': n}] for i, n in enumerate(atoms.arrays['numbers'])]
    G.add_nodes_from(nodes)
    return G

def Compare_graphs(atoms1,atoms2, skin=0.1):
    #only judge isomorphic through only node, node attributes (atomic numbers),  edge.
    global nm
    return is_isomorphic(GraphWithNodes(atoms1, skin=skin),GraphWithNodes(atoms2, skin= skin), node_match=nm)

def plt_graph(atoms, skin=0.1, seed=271):
    atoms = ase.io.read(atoms)
    G = GraphWithNodes(atoms, skin=skin)
    node_color = [i[1]['number'] for i in  G.nodes.data()]
    labeldict = dict(zip(G.nodes.keys(),atoms.get_chemical_symbols()))
    pos = nx.spring_layout(G, seed=seed)
    nx.draw(G, pos,node_color = node_color,with_labels=True, labels = labeldict)
    plt.show()


def Compare_edges(atoms1, atoms2, skin=0.1):
    atoms1 = ase.io.read(atoms1)
    atoms2 = ase.io.read(atoms2)
    G1 = GraphWithNodes(atoms1, skin=skin)
    G2 = GraphWithNodes(atoms2, skin=skin)
    list1=[] ; list2=[]
    for i in range(len(G1.nodes)):
        list1.append(len(G1.edges(i)))
        list2.append(len(G2.edges(i)))
    dif_dict = {}
    for j in range(len(list1)):
        if list1[j] == list2[j]:
            pass
        else:
            dif_dict['{}'.format(j)] = [list1[j],list2[j]]
    return dif_dict






