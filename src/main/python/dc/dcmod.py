from PIL import Image
import pygame,math
from cmath import polar
pygame.init()

#Typical values
xrange=7
yrange=6
scale=0.6
size=(700,600)
antialias_factor=1

def hsla(h,s,l,a=0):
    color=pygame.Color(0)
    color.hsla=h,s,l,a
    return color

def get_color(f,x,y,scale):
    mag,arg=polar(f(complex(x,y)))

    if (mag>2 or mag<1) and mag!=0: #Discontinuous adjustment
        mag=mag/2**math.floor(math.log2(mag))
        
    H=math.degrees(arg)
    if H<0:
        H=360+H
    L=100*(1-scale**mag)
    
    return hsla(H,100,L)

def color_it(xrange,yrange,scale,size,aafactor,f):
    w,h=size[0]*aafactor,size[1]*aafactor
    arr=[]
    for y in range(h):
        row=[]
        for x in range(w):
            xvar=(x-w//2)*xrange/w
            yvar=(-y+h//2)*yrange/h
            col=get_color(f,xvar,yvar,scale)
            arr.append((col.r,col.g,col.b))
    img=Image.new("RGB",(w,h))
    img.putdata(arr)
    img=img.resize((w//aafactor,h//aafactor),resample=Image.ANTIALIAS)
    
    return img

