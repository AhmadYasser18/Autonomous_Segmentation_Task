import numpy as np
import matplotlib.pyplot as plt
import math
##################

def getting_file():
    """function asks for a text file and returns a list containing the values"""

    file_name=input("Enter file name.\nMake sure to write it correctly.\n")
    file=open(file_name,"r").readlines()

    file_content=[]

    for line in file:
        if line != '':
            a=line.strip()
            a=float(a)
            file_content.append(a)

    return file_content

object=0
def add_new(x,y,obj,cel):
    global object
    object=obj
    object+=1
    cel[y][x]=object

##################

class Scans:

    def __init__(self,range=20):
        self.range=range    #the LIDAR's default range is 20

        self.polar=getting_file()

        self.cartesian_x,self.cartesian_y=self.get_cartesian()
        self.cartesian=list(zip(self.cartesian_x,self.cartesian_y))
        self.cells=self.mark_readings()

    def get_cartesian(self):
        #converting from polar to cartesian
        cart_x=[]
        cart_y=[]
        for angle,magn in enumerate(self.polar):
            cart_x.append(magn*math.cos(angle*math.pi/180))
            cart_y.append(magn*math.sin(angle*math.pi/180))

        cart_x=np.array(cart_x)
        cart_y=np.array(cart_y)

        cart_x=np.rint(cart_x)
        cart_y=np.rint(cart_y)

        return cart_x,cart_y

    def plotting(self):
        plt.scatter(self.cartesian_x,self.cartesian_y)

        #Setting max range of the LIDAR on the plot
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        plt.xlim(-self.range,self.range)
        plt.ylim(ymin,self.range)

        plt.grid()
        plt.show()

    def check(self,dict):
        loop=0
        for i,z in dict.items():
            loop+=1
            if i>1 and i-1 not in dict.keys():
                dict[i-1]=z
                del dict[i]
                break
        return dict,loop


    def mark_readings(self):
        self.cells=[[0 for i in range(2*self.range)] for i in range(self.range)]

        for c in self.cartesian:
            if c[0] !=0 or c[1]!=0:
                x=int(c[0])+20
                y=int(c[1])
                self.cells[y][x]=1

        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if self.cells[y][x]==1:
                    if x==0 :
                        if y==0 :
                            add_new(x,y,object,self.cells)

                        elif self.cells[y-1][x] ==0:
                            add_new(x,y,object,self.cells)

                        else:
                            obj=self.cells[y-1][x]
                            self.cells[y][x]=obj

                    elif self.cells[y][x-1] ==0 and self.cells[y-1][x] ==0:
                            add_new(x,y,object,self.cells)

                    elif self.cells[y-1][x] !=0:
                            obj=self.cells[y-1][x]
                            self.cells[y][x]=obj

                    elif self.cells[y][x-1] !=0:
                            obj=self.cells[y][x-1]
                            self.cells[y][x]=obj

        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])-1):
                if self.cells[y][x]>0 and self.cells[y][x+1]>0 and self.cells[y][x]>self.cells[y][x+1]:
                    self.cells[y][x]=self.cells[y][x+1]

        dict_1={}
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if self.cells[y][x]>0:
                    if self.cells[y][x] not in dict_1.keys():
                        dict_1[self.cells[y][x]]=[]
                    dict_1[self.cells[y][x]].append((x,y))

        l=len(dict_1)
        dict_1,turn=self.check(dict_1)
        while l>turn:
            dict_1,turn=self.check(dict_1)

        for key in dict_1.keys():
            for val in dict_1[key]:
                x=val[0]
                y=val[1]
                self.cells[y][x]=key


        return self.cells


    def making_file(self):
        cell=open("cells.txt","w")
        for y in self.cells:
            for c in y:
                if c==0  :
                    cell.write(" .")
                else:
                    cell.write(f" {c}")
            cell.write("\n")
        cell.close()
        print("\nDone making the text file.\n")
##################

scan=Scans()
scan.making_file()

answer=input("Would you like to view the points plotted on a graph?\nEnter Yes or No.\n").strip()
if answer.lower()=="yes":
    scan.plotting()
