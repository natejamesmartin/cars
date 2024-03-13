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
# * 2-way traffic - DONE
# * four-way intersection add oncoming traffic vertically - DONE

# TO TRY
# * multiple lanes
# * merge lanes
# * left-turn lanes
# * exit lanes

# TO FIX

import matplotlib.pyplot as plt
from matplotlib import animation
from numpy import random
import numpy as np
from road import *

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
            

w=world()

r1=road_segment(-200,-5,-5,-5,2,20)
i1=new_intersection()
i1.add_road_start(r1)
i0=new_intersection()
i0.add_road_end(r1)
r1.add_trafficlight()

r2=road_segment(-5,5,-200,5,2,20)
i0.add_road_start(r2)
i2=new_intersection()
i2.add_road_end(r2)

r3=road_segment(-5,200,-5,5,2,20)
i3=new_intersection()
i3.add_road_start(r3)
i0.add_road_end(r3)
r3.add_trafficlight()

r4=road_segment(5,5,5,200,2,20)
i0.add_road_start(r4)
i4=new_intersection()
i4.add_road_end(r4)

r5=road_segment(200,5,5,5,2,20)
i5=new_intersection()
i5.add_road_start(r5)
i0.add_road_end(r5)
r5.add_trafficlight()

r6=road_segment(5,-5,200,-5,2,20)
i0.add_road_start(r6)
i6=new_intersection()
i6.add_road_end(r6)

r7=road_segment(5,-200,5,-5,2,20)
i7=new_intersection()
i7.add_road_start(r7)
i0.add_road_end(r7)
r7.add_trafficlight()

r8=road_segment(-5,-5,-5,-200,2,20)
i0.add_road_start(r8)
i8=new_intersection()
i8.add_road_end(r8)

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

w.add_road_segment(r8)
w.add_intersection(i8)

n_cars=3
dt=0.1 # s

w.road_segments[0].carlist.initialize(n_cars)
#w.road_segments[2].carlist.initialize(3)
#w.road_segments[1].carlist.initialize(3)
#w.road_segments[3].carlist.initialize(3)

#w.initialize_lights()
i0.initialize_lights([[r1,r5],[r3,r7]])
r1.add_oncoming(r5)
r5.add_oncoming(r1)

n_steps=100000

# funcanimation loop, which controls the main event loop, now

w.draw()
#plt.xlim(-200,200)
#plt.ylim(-200,200)
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

speed_factor=1 # 1000 is real time, smaller to go faster
# set repeat = True to run forever
ani=animation.FuncAnimation(fig,animate,frames=n_steps,
                            interval=dt*speed_factor,blit=True,repeat=False)

# uncomment the following lines to save mp4
ani.save('four-way_intersection.mp4',fps=30,extra_args=['-vcodec','libx264'])
del ani
plt.clf()
# otherwise comment out the following line to display movie live
#plt.show()
w.printstats()
w.drawstats()
