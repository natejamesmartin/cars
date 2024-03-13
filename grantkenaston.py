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

r1=road_segment(-15,65,-15,15,2,20)
i1=new_intersection()
i2=new_intersection()
i1.add_road_start(r1)
i2.add_road_end(r1)

r2=road_segment(-10,215,-10,15,2,20)
i0=new_intersection()
i3=new_intersection()
i3.add_road_start(r2)
i0.add_road_end(r2)
r2.add_trafficlight()

r3=road_segment(-5,215,-5,15,2,20)
i4=new_intersection()
i4.add_road_start(r3)
i0.add_road_end(r3)
r3.add_trafficlight()

r4=road_segment(0,65,0,15,2,20)
i5=new_intersection()
i5.add_road_start(r4)
i0.add_road_end(r4)
r4.add_trafficlight()

r5=road_segment(5,15,5,215,2,20)
i6=new_intersection()
i0.add_road_start(r5)
i6.add_road_end(r5)

r6=road_segment(10,15,10,215,2,20)
i7=new_intersection()
i0.add_road_start(r6)
i7.add_road_end(r6)

r7=road_segment(15,15,15,65,2,20)
i8=new_intersection()
i9=new_intersection()
i9.add_road_start(r7)
i8.add_road_end(r7)

r8=road_segment(65,15,15,15,2,20)
i10=new_intersection()
i10.add_road_start(r8)
i9.add_road_end(r8)

r9=road_segment(215,10,15,10,2,20)
i11=new_intersection()
i11.add_road_start(r9)
i0.add_road_end(r9)
r9.add_trafficlight()

r10=road_segment(215,5,15,5,2,20)
i12=new_intersection()
i12.add_road_start(r10)
i0.add_road_end(r10)
r10.add_trafficlight()

r11=road_segment(65,0,15,0,2,20)
i13=new_intersection()
i13.add_road_start(r11)
i0.add_road_end(r11)
r11.add_trafficlight()

r12=road_segment(15,-5,215,-5,2,20)
i14=new_intersection()
i0.add_road_start(r12)
i14.add_road_end(r12)

r13=road_segment(15,-10,215,-10,2,20)
i15=new_intersection()
i0.add_road_start(r13)
i15.add_road_end(r13)

r14=road_segment(15,-15,65,-15,2,20)
i16=new_intersection()
i17=new_intersection()
i17.add_road_start(r14)
i16.add_road_end(r14)

r15=road_segment(15,-65,15,-15,2,20)
i18=new_intersection()
i18.add_road_start(r15)
i16.add_road_end(r15)

r16=road_segment(10,-215,10,-15,2,20)
i19=new_intersection()
i19.add_road_start(r16)
i0.add_road_end(r16)
r16.add_trafficlight()

r17=road_segment(5,-215,5,-15,2,20)
i20=new_intersection()
i20.add_road_start(r17)
i0.add_road_end(r17)
r17.add_trafficlight()

r18=road_segment(0,-65,0,-15,2,20)
i21=new_intersection()
i21.add_road_start(r18)
i0.add_road_end(r18)
r18.add_trafficlight()

r19=road_segment(-5,-15,-5,-215,2,20)
i22=new_intersection()
i0.add_road_start(r19)
i22.add_road_end(r19)

r20=road_segment(-10,-15,-10,-215,2,20)
i23=new_intersection()
i0.add_road_start(r20)
i23.add_road_end(r20)

r21=road_segment(-15,-15,-15,-65,2,20)
i24=new_intersection()
i25=new_intersection()
i25.add_road_start(r21)
i24.add_road_end(r21)

r22=road_segment(-65,-15,-15,-15,2,20)
i26=new_intersection()
i26.add_road_start(r22)
i25.add_road_end(r22)

r23=road_segment(-215,-10,-15,-10,2,20)
i27=new_intersection()
i27.add_road_start(r23)
i0.add_road_end(r23)
r23.add_trafficlight()

r24=road_segment(-215,-5,-15,-5,2,20)
i28=new_intersection()
i28.add_road_start(r24)
i0.add_road_end(r24)
r24.add_trafficlight()

r25=road_segment(-65,0,-15,0,2,20)
i29=new_intersection()
i29.add_road_start(r25)
i0.add_road_end(r25)
r25.add_trafficlight()

r26=road_segment(-15,5,-215,5,2,20)
i30=new_intersection()
i0.add_road_start(r26)
i30.add_road_end(r26)

r27=road_segment(-15,10,-215,10,2,20)
i31=new_intersection()
i0.add_road_start(r27)
i31.add_road_end(r27)

r28=road_segment(-15,15,-65,15,2,20)
i32=new_intersection()
i2.add_road_start(r28)
i32.add_road_end(r28)

w.add_road_segment(r1)
w.add_road_segment(r2)
w.add_road_segment(r3)
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

w.add_intersection(i0)
w.add_intersection(i1)
w.add_intersection(i2)
w.add_intersection(i3)
w.add_intersection(i4)
w.add_intersection(i5)
w.add_intersection(i6)
w.add_intersection(i7)
w.add_intersection(i8)
w.add_intersection(i9)
w.add_intersection(i10)
w.add_intersection(i11)
w.add_intersection(i12)
w.add_intersection(i13)
w.add_intersection(i14)
w.add_intersection(i15)
w.add_intersection(i16)
w.add_intersection(i17)
w.add_intersection(i18)
w.add_intersection(i19)
w.add_intersection(i20)
w.add_intersection(i21)
w.add_intersection(i22)
w.add_intersection(i23)
w.add_intersection(i24)
w.add_intersection(i25)
w.add_intersection(i26)
w.add_intersection(i27)
w.add_intersection(i28)
w.add_intersection(i29)
w.add_intersection(i30)
w.add_intersection(i31)
w.add_intersection(i32)

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
