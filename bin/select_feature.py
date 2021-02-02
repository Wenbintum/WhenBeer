#!/usr/bin/env python
import os,sys
import numpy as np
import matplotlib.pyplot as plt

pathway=os.getcwd()
#pathway='/home/will/Test/class_all_2r_4d'
# folnames

folname = pathway.split('/')[-1]
dimension = int(folname[-2])

os.chdir(pathway)
#1. go to model folder find top0100_001d
ranking_list=[]

with open('models/top0100_00{}d'.format(dimension),'r') as input_file:
    lines=input_file.readlines()

     #2. pick up the first 10 ranking combination
    for i in range(1,11):
        index_com = lines[i].replace('(','').replace(')','').split()[-dimension:]
        ranking_list.append(index_com)

#4. go to feature_space and find feature replacing com_list to real_list
real_list = []
with open('feature_space/Uspace.name','r') as input_file:
    lines=input_file.readlines()
    com_list= np.array(ranking_list).flatten()
    for n in range(len(com_list)):
        real_list.append(lines[int(com_list[n])].split()[0])
    #print str(real_list)
    
#5.find unreapting feature  and corresponding number
full_list= ['WF', 'CTE1' ,'CTE2', 'FE', 'd_c', 'Wd', 'Sd', 'Sd2', 'Kd', 'Kd2', 
            'UN1', 'UN2', 'Eg_c', 'T2g_c', 'O2p_c', 'Md', 'M2p', 'PE', 'IP', 
            'EA', 'ME', '1fold', 'iso_corr', 'd1', 'd2', 'd3', 'dm', 'Rm', 'Q1',
            'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Vad2', 'd_f', 'Eg_f', 'T2g_f', 'O2p_f', 
            'FC', 'bader_charge', 'aver_metal', 'aver_O2p', 'Dos_fermi', 'O2p_fermi','CTE','und_c','CT1']

unique_feature=[]
number_feature=[]
for i in full_list:
    if str(real_list).find(i) != -1:
        unique_feature.append(i)
        number_feature.append(str(real_list).count(i))
        
#print unique_feature, number_feature
dic_feature = dict(zip(unique_feature,number_feature))
dic_feature = sorted(dic_feature.items(), key=lambda x:x[1],reverse=True)
print np.array(dic_feature)[:,1].astype(int) #conver string to int
print range(len(np.array(dic_feature)[:,1]))
plt.bar( range(len(np.array(dic_feature)[:,1])),np.array(dic_feature)[:,1].astype(int),
         tick_label=np.array(dic_feature)[:,0])
plt.figure(figsize=(200,100))
plt.savefig('/p/project/lmcat/wenxu/data/picture/{}.jpg'.format(folname),dpi=300)
