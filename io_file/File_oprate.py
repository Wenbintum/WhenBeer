def split_name(folname):
    '''
    split the name of folder     if name_list[0].startswith('W'): 
       met=name_list[0][:1]
       site=name_list[0][1:]
    else:
       met=name_list[0][:2]
       site=name_list[0][2:]
    r
    and return the metal, site, automatically   
    '''
    name_list=folname.split('O')
    if name_list[0].startswith('W'): 
       met=name_list[0][:1]
       site=name_list[0][1:]
    else:
       met=name_list[0][:2]
       site=name_list[0][2:]
    return met, site

def read_data(output_name):
    with open('{}'.format(output_name),'r') as input_file:
         lines=input_file.readlines()
         if len(lines) < 1:
            line=0.0
         else:
            line =lines[-1].split()
         return line

