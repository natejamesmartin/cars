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

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
            

w=world()

grantkenaston=gk(w,100,300)
grantkenaston2=gk(w,100,-300)

def link_ns(gk1,gk2,w):
    # link r6ro and r6lo of gk1 to r1ri and r1li of gk2

    startx=gk1.r6ro.endx
    starty=gk1.r6ro.endy
    endx=gk2.r1ri.startx
    endy=gk2.r1ri.starty
    print(startx,starty,endx,endy)
    sixtyonelinker_right=road_segment(startx,starty,endx,endy,2,20)
    w.add_road_segment(sixtyonelinker_right)
    gk1.i6rd.add_road_start(sixtyonelinker_right)
    gk2.i1rc.add_road_end(sixtyonelinker_right)

    startx=gk1.r6lo.endx
    starty=gk1.r6lo.endy
    endx=gk2.r1li.startx
    endy=gk2.r1li.starty
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
    print(startx,starty,endx,endy)
    twentyfivelinker_right=road_segment(startx,starty,endx,endy,2,20)
    w.add_road_segment(twentyfivelinker_right)
    gk2.i2rd.add_road_start(twentyfivelinker_right)
    gk1.i5rc.add_road_end(twentyfivelinker_right)

    startx=gk2.r2lo.endx
    starty=gk2.r2lo.endy
    endx=gk1.r5li.startx
    endy=gk1.r5li.starty
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

n_steps=100000

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

speed_factor=10 # 1000 is real time, smaller to go faster
# set repeat = True to run forever
ani=animation.FuncAnimation(fig, animate, frames=n_steps,
                            interval=dt*speed_factor, blit=True,repeat=False)

# uncomment the following lines to save mp4
#ani.save('grantkenaston_new2.mp4',fps=30,extra_args=['-vcodec','libx264'])
#del ani
#plt.clf()
# otherwise comment out the following line to display movie live
plt.show()
w.printstats()
w.drawstats()
