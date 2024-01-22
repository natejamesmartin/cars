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
from math import sqrt
import numpy as np
from road import *

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')


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

#ani.save('fewer_collisions.mp4',fps=30,extra_args=['-vcodec','libx264'])

plt.show()
