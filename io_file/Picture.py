from ase.io import read,write
import sys,os
from PIL import Image,ImageFont,ImageDraw
def get_top(folname,filename='opt.traj'):
    """
    this function is to gennerate a series of picture with topview configuration
    Input:
    -
    Output:
    -
    """
    atoms=read(filename)
    write('{}T.png'.format(folname), atoms)
    write('{}S.png'.format(folname), atoms, rotation='-90x')

def add_text(picname,content,x_position=0.1, y_position=0):
    """
    img.size will return a tuple (a,b)
    """
    img = Image.open(picname) 
     
    draw = ImageDraw.Draw(img) 
     
    font = ImageFont.truetype("/p/project/lmcat/wenxu/scripts/will_package/parameter/arial.ttf", 25) 
     
    draw.text((img.size[0]*x_position, img.size[1]*y_position),content,(0,0,0),font=font) 
     
    img.save('{}'.format(picname))  #there is no  png keyword 
    #img  = Image.open(picname)
    #draw = ImageDraw.Draw(img)
    #font = ImageFont.truetype("/p/project/lmcat/wenxu/scripts/will_package/parameter/arial.ttf", size=20)
    #draw.text((img.size[0]*x_position, img.size[1]*y_position),content,(0,0,0),front=font)
    #img.save('{}'.format(picname)) 
#generate HD picture with high light  
