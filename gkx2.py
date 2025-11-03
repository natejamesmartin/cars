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
# * collision avoidance looking ahead to next road segment - DONE
# * 2-way traffic - STARTED 4-way intersection - DONE

# TO TRY
# * multiple lanes
# * merge lanes

# TO FIX
# * slow moving cars dont get close to one another

import matplotlib.pyplot as plt
from matplotlib import animation
from numpy import random
import numpy as np
from road import *
import argparse
from CLVars import parse_my_args
import CLVars
import carlist

args = parse_my_args()

#parser = argparse.ArgumentParser()
#parser.add_argument('-v','--verbose',type=int)
#parser.add_argument('-m','--movie')
#parser.add_argument('-t','--carnum')
#args = parser.parse_args()



fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(8, 6))


            

w=world()

grantkenaston=gk(w,100,300)
grantkenaston2=gk(w,100,-300)

def link_ns(gk1,gk2,w):
    # link r6ro and r6lo of gk1 to r1ri and r1li of gk2

    startx=gk1.r6ro.endx
    starty=gk1.r6ro.endy
    endx=gk2.r1ri.startx
    endy=gk2.r1ri.starty
    if(args.verbose == 1):
         print(startx,starty,endx,endy)
    sixtyonelinker_right=road_segment(startx,starty,endx,endy,2,20)
    w.add_road_segment(sixtyonelinker_right)
    gk1.i6rd.add_road_start(sixtyonelinker_right)
    gk2.i1rc.add_road_end(sixtyonelinker_right)

    startx=gk1.r6lo.endx
    starty=gk1.r6lo.endy
    endx=gk2.r1li.startx
    endy=gk2.r1li.starty
    if(args.verbose == 1):
        print(startx,starty,endx,endy)
    sixtyonelinker_left=road_segment(startx,starty,endx,endy,2,20)
    w.add_road_segment(sixtyonelinker_left)
    gk1.i6ld.add_road_start(sixtyonelinker_left)
    gk2.i1lc.add_road_end(sixtyonelinker_left)

    # link r2ro and r2lo of gk2 to r5ri and r5li of gk1

    startx=gk2.r2ro.endx
    starty=gk2.r2ro.endy
    endx=gk1.r5ri.startx
    endy=gk1.r5ri.starty
    if(args.verbose==1):
        print(startx,starty,endx,endy)
    twentyfivelinker_right=road_segment(startx,starty,endx,endy,2,20)
    w.add_road_segment(twentyfivelinker_right)
    gk2.i2rd.add_road_start(twentyfivelinker_right)
    gk1.i5rc.add_road_end(twentyfivelinker_right)

    startx=gk2.r2lo.endx
    starty=gk2.r2lo.endy
    endx=gk1.r5li.startx
    endy=gk1.r5li.starty
    if(args.verbose==1):
        print(startx,starty,endx,endy)
    twentyfivelinker_left=road_segment(startx,starty,endx,endy,2,20)
    w.add_road_segment(twentyfivelinker_left)
    gk2.i2ld.add_road_start(twentyfivelinker_left)
    gk1.i5lc.add_road_end(twentyfivelinker_left)

link_ns(grantkenaston,grantkenaston2,w)

n_cars=3
dt=0.1 # s

w.road_segments[0].carlist.initialize(n_cars)
#w.road_segments[2].carlist.initialize(3)
#w.road_segments[1].carlist.initialize(3)
#w.road_segments[3].carlist.initialize(3)

w.initialize_lights()
#i0.initialize_lights([[r1,r5],[r3,r7]])
#r1.add_oncoming(r5)
#r5.add_oncoming(r1)

n_steps=args.nsteps

# funcanimation loop, which controls the main event loop, now

w.draw(ax)
timebox=ax.text(0.01,0.99,"Time: %6.2f s"%(0),
                 ha='left',va='top',transform=ax.transAxes)
global_time=0
xFuel = []
yFuel = []
xKE = []
yKE = []

ax.set_xlabel("distance (m)")
ax.set_ylabel("distance (m)")

def animate(i):
    global global_time,w,timebox
    if(args.verbose==1):
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

def init():
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Fuel (L)")
    ax2.set_xlim(0,30)
    ax2.set_ylim(0,0.02)
    del xFuel[:]
    del yFuel[:]
    line.set_data(xFuel,yFuel)
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Speed (m/s)")
    ax3.set_xlim(0,30)
    ax3.set_ylim(0,30)
    del xKE[:]
    del yKE[:]
    ax2.set_title("Fuel Consumption")
    ax3.set_title("Speed")
    return line, line2,

line, = ax2.plot([],[],lw=2)
line2, = ax3.plot([],[],lw=2)

def animate2(i):
    found_car = w.find_car()
    t = -1
    fuel = -1
    if(found_car != None):
        t = found_car.time
        fuel = found_car.fuel
        v = found_car.v
        xFuel.append(t)
        yFuel.append(fuel)
        xKE.append(t)
        yKE.append(v)
    line.set_data(xFuel,yFuel)
    line2.set_data(xKE,yKE)
    xmin, xmax = ax2.get_xlim()
    if t >= xmax:
        ax2.set_xlim(xmin, 2*xmax)
    ymin, ymax = ax2.get_ylim()
    if fuel >= ymax:
        ax2.set_ylim(ymin, 2*ymax)
    xmin, xmax = ax3.get_xlim()
    if t >= xmax:
        ax3.set_xlim(xmin, 2*xmax)

    return line, line2,

speed_factor=10 # 1000 is real time, smaller to go faster
# set repeat = True to run forever

ani=animation.FuncAnimation(fig, animate, frames=n_steps,
                            interval=dt*speed_factor, blit=False,repeat=False)

if(args.carnum!=-1):
    ani2 = animation.FuncAnimation(fig2,animate2,frames=n_steps,
                                   interval = dt*speed_factor,
                                   init_func=init, blit=False)


# uncomment the following lines to save mp4 (if -m)
if(args.movie == True):
    ani.save('gkx2.mp4',fps=30,extra_args=['-vcodec','libx264'])
    del ani
    plt.clf()
# otherwise comment out the following line to display movie live
else:
    plt.show()
    w.printstats()
    w.drawstats()
