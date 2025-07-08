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

# TO TRY
# * 2-way traffic - STARTED 4-way intersection
# * multiple lanes
# * merge lanes

# TO FIX
# * four-way intersection add oncoming traffic vertically

import matplotlib.pyplot as plt
from matplotlib import animation
from numpy import random
import numpy as np
from road import *

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
            

w=world()

# roads entering nw
r1rs=road_segment(-15,65,-15,15,2,20)   # road 1, right slip
r1ri=road_segment(-10,215,-10,65,2,20)  # road 1, right input
r1ro=road_segment(-10,65,-10,15,2,20)   # road 1, right output
r1ro.add_trafficlight()
r1li=road_segment(-5,215,-5,65,2,20)    # road 1, left input
r1lo=road_segment(-5,65,-5,15,2,20)     # road 1, left output
r1lo.add_trafficlight()
r1lt=road_segment(0,65,0,15,2,20)       # road 1, left turn
r1lt.add_trafficlight()

# intersections inside road 1
i1rc=new_intersection()                 # road 1, right creator
i1lc=new_intersection()                 # road 1, left creator
i1rs=new_intersection()                 # road 1, right slip
i1lt=new_intersection()                 # road 1, left turn

# hook these up
i1rc.add_road_start(r1ri)
i1lc.add_road_start(r1li)
i1rs.add_road_end(r1ri)
i1rs.add_road_start(r1rs)
i1rs.add_road_start(r1ro)
i1lt.add_road_end(r1li)
i1lt.add_road_start(r1lo)
i1lt.add_road_start(r1lt)

# intersections connecting road 1 to other roads
i18rs=new_intersection()    # road 1 to 8, right slip to right slip
i16ll=new_intersection()    # road 1 to 6, left output to left output
i16rl=new_intersection()    # road 1 to 6, right output to right input
i14lt=new_intersection()    # road 1 to 4, left turn to left output/right input

# hook these up later...

# roads leaving ne
r2lo=road_segment(5,15,5,215,2,20)      # road 2, left output
r2ri=road_segment(10,15,10,65,2,20)     # road 2, right input
r2ro=road_segment(10,65,10,215,2,20)    # road 2, right output
r2rs=road_segment(15,15,15,65,2,20)     # road 2, right slip

# intersections inside road 2
i2ld=new_intersection()                 # road 2, left destroyer
i2rd=new_intersection()                 # road 2, right destroyer
i2rs=new_intersection()                 # road 2, right slip

# hook these up
i2ld.add_road_end(r2lo)
i2rd.add_road_end(r2ro)
i2rs.add_road_end(r2ri)
i2rs.add_road_end(r2rs)
i2rs.add_road_start(r2ro)

# intersections feeding into road 2 are defined and connected at feeding road

# roads entering ne
r8=road_segment(65,15,15,15,2,20)
r9=road_segment(215,10,65,10,2,20)
r9prime=road_segment(65,10,15,10,2,20)
r9prime.add_trafficlight()
r10=road_segment(215,5,65,5,2,20)
r10prime=road_segment(65,5,15,5,2,20)
r10prime.add_trafficlight()
r11=road_segment(65,0,15,0,2,20)
r11.add_trafficlight()

# roads leaving se
r12=road_segment(15,-5,215,-5,2,20)
r13=road_segment(15,-10,65,-10,2,20)
r13prime=road_segment(65,-10,215,-10,2,20)
r14=road_segment(15,-15,65,-15,2,20)

# roads entering se
r15=road_segment(15,-65,15,-15,2,20)
r16=road_segment(10,-215,10,-65,2,20)
r16prime=road_segment(10,-65,10,-15,2,20)
r16prime.add_trafficlight()
r17=road_segment(5,-215,5,-65,2,20)
r17prime=road_segment(5,-65,5,-15,2,20)
r17prime.add_trafficlight()
r18=road_segment(0,-65,0,-15,2,20)
r18.add_trafficlight()

# roads leaving sw
r19=road_segment(-5,-15,-5,-215,2,20)
r20=road_segment(-10,-15,-10,-65,2,20)
r20prime=road_segment(-10,-65,-10,-215,2,20)
r21=road_segment(-15,-15,-15,-65,2,20)

# roads entering sw
r22=road_segment(-65,-15,-15,-15,2,20)
r23=road_segment(-215,-10,-65,-10,2,20)
r23prime=road_segment(-65,-10,-15,-10,2,20)
r23prime.add_trafficlight()
r24=road_segment(-215,-5,-65,-5,2,20)
r24prime=road_segment(-65,-5,-15,-5,2,20)
r24prime.add_trafficlight()
r25=road_segment(-65,0,-15,0,2,20)
r25.add_trafficlight()

# roads leaving nw
r26=road_segment(-15,5,-215,5,2,20)
r27=road_segment(-15,10,-65,10,2,20)
r27prime=road_segment(-65,10,-215,10,2,20)
r28=road_segment(-15,15,-65,15,2,20)

w.add_road_segment(r1)
w.add_road_segment(r2)
w.add_road_segment(r2prime)
w.add_road_segment(r3)
w.add_road_segment(r3prime)
w.add_road_segment(r4)
w.add_road_segment(r5)
w.add_road_segment(r6)
w.add_road_segment(r7)
w.add_road_segment(r8)
w.add_road_segment(r9)
w.add_road_segment(r10)
w.add_road_segment(r11)
w.add_road_segment(r12)
w.add_road_segment(r13)
w.add_road_segment(r14)
w.add_road_segment(r15)
w.add_road_segment(r16)
w.add_road_segment(r17)
w.add_road_segment(r18)
w.add_road_segment(r19)
w.add_road_segment(r20)
w.add_road_segment(r21)
w.add_road_segment(r22)
w.add_road_segment(r23)
w.add_road_segment(r24)
w.add_road_segment(r25)
w.add_road_segment(r26)
w.add_road_segment(r27)
w.add_road_segment(r28)

#w.add_intersection(i0)
#w.add_intersection(i1)
#w.add_intersection(i2)
#w.add_intersection(i3)
#w.add_intersection(i4)

n_cars=3
dt=0.1 # s

w.road_segments[0].carlist.initialize(n_cars)
#w.road_segments[2].carlist.initialize(3)
#w.road_segments[1].carlist.initialize(3)
#w.road_segments[3].carlist.initialize(3)

#w.initialize_lights()
#i0.initialize_lights([[r1,r5],[r3,r7]])
r1.add_oncoming(r5)
r5.add_oncoming(r1)

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

speed_factor=500 # 1000 is real time, smaller to go faster
# set repeat = True to run forever
ani=animation.FuncAnimation(fig, animate, frames=n_steps,
                            interval=dt*speed_factor, blit=True,repeat=False)

#ani.save('grantkenaston.mp4',fps=30,extra_args=['-vcodec','libx264'])

plt.show()
