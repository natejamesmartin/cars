#!/usr/bin/python3

# Ideas

# DONE
# * acceleration on merge - DONE
# * collision avoidance - DONE
# * different speeds - DONE
# * turning into intersecting road - DONE
# * 2 perpendicular roads - DONE
# * different parameters - DONE
# * put time in video - DONE
# * reinstating a car creator - DONE
# * stop signs - DONE
# * traffic lights - DONE
# * trying different geometries - DONE

# TO TRY
# * 2-way traffic
# * multiple lanes
# * merge lanes

# TO FIX
# * collision avoidance looking ahead to next road segment

import matplotlib.pyplot as plt
from matplotlib import animation
from carlist import car
from carlist import carlist
from numpy import random
from celluloid import Camera
from math import sqrt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
camera = Camera(fig)

class road:
    def __init__(self):
        self.start=0
        self.end=400

class intersection:
    def __init__(self):
        self.pos=200
        self.nwaiting=20
    def removecar(self):
        self.nwaiting-=1

import itertools
        
class road_segment:

    id_iter=itertools.count()

    def __init__(self,startx,starty,endx,endy,n_lanes,vlimit):
        self.startx=startx
        self.starty=starty
        self.endx=endx
        self.endy=endy
        dx=self.endx-self.startx
        dy=self.endy-self.starty
        hyp=sqrt(dx**2+dy**2)
        self.length=hyp
        self.unitx=dx/hyp
        self.unity=dy/hyp
        self.n_lanes=n_lanes
        self.vlimit=vlimit
        self.id=next(self.id_iter)
        #self.startint=-1
        #self.endint=-1
        self.carlist=carlist(self)
        self.stopsign=False
        self.trafficlight=False
        self.trafficlightcolor='red'
        self.greentime=50 # s
        self.yellowtime=10 # s
    def add_startint(self,anint):
        self.startint=anint
    def add_endint(self,anint):
        self.endint=anint
    def add_stopsign(self):
        self.stopsign=True
    def add_trafficlight(self):
        self.trafficlight=True

class new_intersection:
    id_iter=itertools.count()
    def __init__(self):
        self.road_ends=[]
        self.road_starts=[]
        self.id=next(self.id_iter)
        self.trafficlights=[]
        self.cycletime=0 # s
        self.intersectiontime=0 # s
    def add_road_start(self,seg):
        self.road_starts.append(seg)
        seg.add_startint(self)
    def add_road_end(self,seg):
        self.road_ends.append(seg)
        seg.add_endint(self)        
    def x(self):
        for seg in self.road_starts:
            x=seg.startx
        for seg in self.road_ends:
            x=seg.endx
        return x
    def y(self):
        for seg in self.road_starts:
            y=seg.starty
        for seg in self.road_ends:
            y=seg.endy
        return y
    def list_starts(self):
        l=[]
        for seg in self.road_starts:
            l.append(seg.id)
        return l
    def list_ends(self):
        l=[]
        for seg in self.road_ends:
            l.append(seg.id)
        return l
    def is_creator(self):
        if len(self.road_starts)>0 and len(self.road_ends)==0:
            return True
        else:
            return False
    def is_destroyer(self):
        if len(self.road_ends)>0 and len(self.road_starts)==0:
            return True
        else:
            return False
    def step(self,dt):
        self.intersectiontime+=dt

        if self.intersectiontime>self.cycletime:
            self.intersectiontime=0

        checktimelow=0
        checktimehigh=0
        greeni=-1
        yellowi=-1
        for i,light in enumerate(self.trafficlights):
            checktimehigh=checktimelow+light.greentime

            if (self.intersectiontime>=checktimelow) & (self.intersectiontime<=checktimehigh):
                greeni=i
            elif (self.intersectiontime>=checktimelow+light.greentime) & (self.intersectiontime<=checktimehigh+light.yellowtime):
                yellowi=i

            checktimelow+=light.greentime+light.yellowtime
        for i,light in enumerate(self.trafficlights):
            light.trafficlightcolor='red'
            if i==greeni:
                light.trafficlightcolor='green'
            elif i==yellowi:
                light.trafficlightcolor='yellow'
                
    def initialize_lights(self):
        self.trafficlights=[]
        for seg in self.road_ends:
            if seg.trafficlight:
                self.trafficlights.append(seg)
                print("adding traffic light")
        for i,light in enumerate(self.trafficlights):
            light.trafficlightcolor='red'
            if i==0:
                light.trafficlightcolor='green'
            self.cycletime+=light.greentime+light.yellowtime
        self.intersectiontime=0

class world:
    def __init__(self):
        self.road_segments=[]
        self.intersections=[]
    def add_road_segment(self,seg):
        self.road_segments.append(seg)
    def add_intersection(self,i):
        self.intersections.append(i)
    def car_data(self):
        # returns where all the cars in the world are
        xs=[]
        ys=[]
        colors=[]
        for seg in self.road_segments:
            xs+=seg.carlist.xs()
            ys+=seg.carlist.ys()
            colors+=seg.carlist.colors()
        return xs,ys,colors
    def lights_data(self):
        # returns where all the lights in the world are
        xs=[]
        ys=[]
        colors=[]
        for seg in self.road_segments:
            if seg.trafficlight:
                xs.append(seg.endx-seg.unitx*20)
                ys.append(seg.endy-seg.unity*20)
                colors.append(seg.trafficlightcolor)
        return xs,ys,colors        

    def draw(self):
        for seg in self.road_segments:
            plt.arrow(seg.startx,seg.starty,seg.endx-seg.startx,seg.endy-seg.starty,width=2,length_includes_head=True,color='black')
            if seg.stopsign:
                plt.scatter(seg.endx-seg.unitx*20,seg.endy-seg.unity*20,marker='8',c='red',s=200)
        #for i in self.intersections:
        #    plt.scatter(i.x(),i.y(),c='red',marker='s')
        xs,ys,colors=self.car_data()
        self.carplot=plt.scatter(xs,ys,c=colors)
        xs,ys,colors=self.lights_data()
        self.lightsplot=plt.scatter(xs,ys,c=colors,marker='s',s=200,zorder=-1)
        
    def verbose_draw(self):
        for seg in self.road_segments:
            plt.arrow(seg.startx,seg.starty,seg.endx-seg.startx,seg.endy-seg.starty,width=10,length_includes_head=True)
            print("This segment has id",seg.id)
            print("This segment starts at intersection",seg.startint)
            print("This segment ends at intersection",seg.endint)
            for c in seg.carlist.carlist:
                print(c.color)
                plt.scatter(c.x,c.y,c=c.color)
        for i in self.intersections:
            print("The id of this intersection is",i.id)
            print("starts",i.list_starts(),"ends",i.list_ends())
            print("This intersection is at x=%f y=%f"%(i.x(),i.y()))
            plt.scatter(i.x(),i.y(),c='black')
            if(i.is_creator()):
                print("This intersection is a creator")
            if(i.is_destroyer()):
                print("This intersection is a destroyer")
    def step(self,dt):
        for seg in self.road_segments:
            seg.carlist.step(dt)
        for i in self.intersections:
            i.step(dt)
    def initialize_lights(self):
        for i in self.intersections:
            i.initialize_lights()
            

w=world()

r1=road_segment(0,0,200,0,2,20)
r2=road_segment(200,0,400,0,2,20)
r2.add_trafficlight()

i0=new_intersection()
i0.add_road_start(r1)

i1=new_intersection()
i1.add_road_end(r1)
i1.add_road_start(r2)

i2=new_intersection()
i2.add_road_end(r2)

r3=road_segment(200,-200,200,0,2,20)
r3.add_stopsign()
i1.add_road_end(r3)
i3=new_intersection()
i3.add_road_start(r3)

r4=road_segment(400,-200,400,0,2,20)
i4=new_intersection()
i4.add_road_start(r4)
i2.add_road_end(r4)
r4.add_trafficlight()

r5=road_segment(400,0,600,0,2,20)
i2.add_road_start(r5)
i5=new_intersection()
i5.add_road_end(r5)

r6=road_segment(600,0,800,0,2,20)
i5.add_road_start(r6)
i6=new_intersection()
i6.add_road_end(r6)

r7=road_segment(600,0,600,200,2,20)
i5.add_road_start(r7)
i7=new_intersection()
i7.add_road_end(r7)

w.add_road_segment(r1)
w.add_road_segment(r2)
w.add_intersection(i0)
w.add_intersection(i1)
w.add_intersection(i2)

w.add_road_segment(r3)
w.add_intersection(i3)

w.add_road_segment(r4)
w.add_intersection(i4)

w.add_road_segment(r5)
w.add_intersection(i5)

w.add_road_segment(r6)
w.add_intersection(i6)

w.add_road_segment(r7)
w.add_intersection(i7)

n_cars=3
dt=0.1 # s

w.road_segments[0].carlist.initialize(n_cars)
#w.road_segments[2].carlist.initialize(3)
#w.road_segments[1].carlist.initialize(3)
#w.road_segments[3].carlist.initialize(3)

w.initialize_lights()

n_steps=3000

# funcanimation loop, which controls the main event loop, now

w.draw()
timebox=plt.text(0.01,0.99,"Time: %6.2f s"%(0),
                 ha='left',va='top',transform=ax.transAxes)
global_time=0

def animate(i):
    global global_time,w,timebox
    print("the time is %6.2f s"%(global_time))
    
    xs,ys,colors=w.car_data()
    scatter=w.carplot
    scatter.set_offsets(np.column_stack([xs,ys]))
    scatter.set_color(colors)

    xs,ys,colors=w.lights_data()
    lightscatter=w.lightsplot
    lightscatter.set_offsets(np.column_stack([xs,ys]))
    lightscatter.set_color(colors)

    timebox.set_text("Time: %6.2f s"%(global_time))
    
    w.step(dt)
    global_time+=dt
    return scatter,lightscatter,timebox,

speed_factor=100 # 1000 is real time, smaller to go faster
# set repeat = True to run forever
ani=animation.FuncAnimation(fig, animate, frames=n_steps,
                            interval=dt*speed_factor, blit=True,repeat=False)

ani.save('fewer_collisions.mp4',fps=30,extra_args=['-vcodec','libx264'])

#plt.show()
