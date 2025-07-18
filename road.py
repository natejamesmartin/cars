from math import sqrt
import itertools
from carlist import carlist
from carlist import car
import matplotlib.pyplot as plt
import parameters
import argparse
from CLVars import parse_my_args

args = parse_my_args()

class road_segment:

    id_iter=itertools.count()

    def __init__(self,startx,starty,endx,endy,n_lanes,vlimit):
        self.startx=startx
        self.starty=starty
        self.endx=endx
        self.endy=endy
        self.n_lanes=n_lanes
        self.vlimit=vlimit
        dx=self.endx-self.startx
        dy=self.endy-self.starty
        hyp=sqrt(dx**2+dy**2)
        self.length=hyp
        self.unitx=dx/hyp
        self.unity=dy/hyp
        self.id=next(self.id_iter)
        #self.startint=-1
        #self.endint=-1
        self.carlist=carlist(self)
        self.stopsign=False
        self.trafficlight=False
        self.trafficlightcolor='red'
        self.greentime=parameters.greentime # s
        self.yellowtime=parameters.yellowtime # s
        self.oncoming=[] # list of oncoming traffic roads
    def add_oncoming(self,road):
        self.oncoming.append(road)
    def add_startint(self,anint):
        self.startint=anint
    def add_endint(self,anint):
        self.endint=anint
    def add_stopsign(self):
        self.stopsign=True
    def add_trafficlight(self):
        self.trafficlight=True
    def displace(self,x0,y0):
        self.startx=self.startx+x0
        self.starty=self.starty+y0
        self.endx=self.endx+x0
        self.endy=self.endy+y0

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
        for i,lights in enumerate(self.trafficlights):
            checktimehigh=checktimelow+lights[0].greentime
            #print("stepping traffic lights",i,self.id)

            if (self.intersectiontime>=checktimelow) & (self.intersectiontime<=checktimehigh):
                greeni=i
            elif (self.intersectiontime>=checktimelow+lights[0].greentime) & (self.intersectiontime<=checktimehigh+lights[0].yellowtime):
                yellowi=i

            checktimelow+=lights[0].greentime+lights[0].yellowtime
        for i,lights in enumerate(self.trafficlights):
            for light in lights:
                light.trafficlightcolor='red'
            if i==greeni:
                for light in lights:
                    light.trafficlightcolor='green'
            elif i==yellowi:
                for light in lights:
                    light.trafficlightcolor='yellow'

    def initialize_lights(self,tietogether=[]):
        if(args.verbose==1):
            print("initializing intersection number",self.id,tietogether)
        self.cycletime=0
        for tiethese in tietogether:
            if(args.verbose==1):
                print("tie the following traffic lights together")
            for seg in tiethese:
                if(args.verbose==1):
                    print(seg.id)
        self.trafficlights=tietogether
        if len(self.trafficlights)==0:
            for seg in self.road_ends:
                if seg.trafficlight:
                    self.trafficlights.append([seg])
                    if(args.verbose==1):
                        print("adding traffic light")
        for i,lights in enumerate(self.trafficlights):
            for light in lights:
                light.trafficlightcolor='red'
                if i==0:
                    light.trafficlightcolor='green'
            self.cycletime+=lights[0].greentime+lights[0].yellowtime
        self.intersectiontime=0

class world:
    def __init__(self):
        self.road_segments=[]
        self.intersections=[]
        self.light_controllers=[]
    def add_road_segment(self,seg):
        self.road_segments.append(seg)
    def add_intersection(self,i):
        self.intersections.append(i)
    def add_light_controller(self,lc):
        self.light_controllers.append(lc)
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
            if(args.verbose==1):
                print("This segment has id",seg.id)
                print("This segment starts at intersection",seg.startint)
                print("This segment ends at intersection",seg.endint)
            for c in seg.carlist.carlist:
                if(args.verbose==1):
                    print(c.color)
                plt.scatter(c.x,c.y,c=c.color)
        for i in self.intersections:
            if(args.verbose==1):
                print("The id of this intersection is",i.id)
                print("starts",i.list_starts(),"ends",i.list_ends())
                print("This intersection is at x=%f y=%f"%(i.x(),i.y()))
            plt.scatter(i.x(),i.y(),c='black')
            if(i.is_creator()):
                if(args.verbose==1):
                    print("This intersection is a creator")
            if(i.is_destroyer()):
                if(args.verbose==1):
                    print("This intersection is a destroyer")
    def step(self,dt):
        for seg in self.road_segments:
            seg.carlist.step(dt)
        for i in self.intersections:
            i.step(dt)
        for lc in self.light_controllers:
            lc.step(dt)
    def initialize_lights(self):
        for lc in self.light_controllers:
            lc.initialize_lights()
    def printstats(self):
        with open('road_stats.out','w') as f:
            f.write("integer creationtime deletiontime lifetime\n")
        for seg in self.road_segments:
            i=seg.endint
            if i.is_destroyer():
                if(args.verbose==1):
                    print("This intersection is at x=%f y=%f"%(i.x(),i.y()))
                seg.carlist.cs.printstats()
                with open('road_stats.out','a') as f:
                    cs=seg.carlist.cs
                    for i,ct in enumerate(cs.creationtimes):
                        f.write("%d %f %f %f\n"%(i,ct,cs.deletiontimes[i],cs.deletiontimes[i]-ct))
    def drawstats(self):
        for seg in self.road_segments:
            i=seg.endint
            if i.is_destroyer():
                if(args.verbose==1):
                    print("This intersection is at x=%f y=%f"%(i.x(),i.y()))
                lifetimes=[]
                cs=seg.carlist.cs
                for i,ct in enumerate(cs.creationtimes):
                    lifetimes.append(cs.deletiontimes[i]-cs.creationtimes[i])
                plt.scatter(cs.creationtimes,lifetimes)
        plt.xlabel('creation time (s)')
        plt.ylabel('lifetime (s)')
        plt.savefig('lt-vs-ct.png')

class light_controller:
    # a light_controller is a list of light_sets and we should cycle
    # through the lights with some times
    def __init__(self):
        self.light_set_list=[]
        self.cycletime=0 # s
        self.intersectiontime=0 # s
    def add_light_set(self,lset):
        self.light_set_list.append(lset)
    def initialize_lights(self):
        self.cycletime=0
        for i,lset in enumerate(self.light_set_list):
            if i==0:
                lset.set_green()
            else:
                lset.set_red()
            self.cycletime+=lset.greentime+lset.yellowtime
        self.intersectiontime=0
    def step(self,dt):
        self.intersectiontime+=dt

        if self.intersectiontime>self.cycletime:
            self.intersectiontime=0
        checktimelow=0
        checktimehigh=0
        greeni=-1
        yellowi=-1
        for i,lset in enumerate(self.light_set_list):
            checktimehigh=checktimelow+lset.greentime
            if (self.intersectiontime>=checktimelow) & (self.intersectiontime<=checktimehigh):
                greeni=i
            elif (self.intersectiontime>=checktimelow+lset.greentime) & (self.intersectiontime<=checktimehigh+lset.yellowtime):
                yellowi=i
            checktimelow+=lset.greentime+lset.yellowtime
        for i,lset in enumerate(self.light_set_list):
            lset.set_red()
            if i==greeni:
                lset.set_green()
            elif i==yellowi:
                lset.set_yellow()
        
        
class light_set:
    # a light_set is a list of roads, with traffic lights, that all
    # should have the same light setting at the same time
    def __init__(self):
        self.trafficlights=[]
        self.greentime=parameters.greentime
        self.yellowtime=parameters.yellowtime
    def add_light(self,seg):
        self.trafficlights.append(seg)
    def set_color(self,color):
        for light in self.trafficlights:
            light.trafficlightcolor=color
    def set_red(self):
        self.set_color('red')
    def set_green(self):
        self.set_color('green')
    def set_yellow(self):
        self.set_color('yellow')

class gk:
    def __init__(self,w,x0=0,y0=0):
        self.light_set_1=light_set()
        self.light_set_2=light_set()
        self.light_controller=light_controller()
        self.light_controller.add_light_set(self.light_set_1)
        self.light_controller.add_light_set(self.light_set_2)
        w.add_light_controller(self.light_controller) # add to the world
        # roads entering nw
        self.r1rs=road_segment(-15,65,-15,15,2,20)   # road 1, right slip
        self.r1ri=road_segment(-10,215,-10,65,2,20)  # road 1, right input
        self.r1ro=road_segment(-10,65,-10,15,2,20)   # road 1, right output
        self.r1ro.add_trafficlight()
        self.light_set_1.add_light(self.r1ro)
        self.r1li=road_segment(-5,215,-5,65,2,20)    # road 1, left input
        self.r1lo=road_segment(-5,65,-5,15,2,20)     # road 1, left output
        self.r1lo.add_trafficlight()
        self.light_set_1.add_light(self.r1lo)
        self.r1lt=road_segment(0,65,0,15,2,20)       # road 1, left turn
        self.r1lt.add_trafficlight()
        self.light_set_1.add_light(self.r1lt)

        self.r1rs.displace(x0,y0)
        self.r1ri.displace(x0,y0)
        self.r1ro.displace(x0,y0)
        self.r1li.displace(x0,y0)
        self.r1lo.displace(x0,y0)
        self.r1lt.displace(x0,y0)
        
        # intersections inside road 1
        self.i1rc=new_intersection()                 # road 1, right creator
        self.i1lc=new_intersection()                 # road 1, left creator
        self.i1rs=new_intersection()                 # road 1, right slip
        self.i1lt=new_intersection()                 # road 1, left turn

        # hook these up
        self.i1rc.add_road_start(self.r1ri)
        self.i1lc.add_road_start(self.r1li)
        self.i1rs.add_road_end(self.r1ri)
        self.i1rs.add_road_start(self.r1rs)
        self.i1rs.add_road_start(self.r1ro)
        self.i1lt.add_road_end(self.r1li)
        self.i1lt.add_road_start(self.r1lo)
        self.i1lt.add_road_start(self.r1lt)

        # intersections connecting road 1 to other roads
        self.i18rsrs=new_intersection()    # road 1 to 8, right slip to right slip
        self.i16lolo=new_intersection()    # road 1 to 6, left output to left output
        self.i16rori=new_intersection()    # road 1 to 6, right output to right input
        self.i14ltlori=new_intersection()    # road 1 to 4, left turn to left output/right input

        # hook these up last

        # roads leaving ne
        self.r2lo=road_segment(5,15,5,215,2,20)      # road 2, left output
        self.r2ri=road_segment(10,15,10,65,2,20)     # road 2, right input
        self.r2ro=road_segment(10,65,10,215,2,20)    # road 2, right output
        self.r2rs=road_segment(15,15,15,65,2,20)     # road 2, right slip

        self.r2lo.displace(x0,y0)
        self.r2ri.displace(x0,y0)
        self.r2ro.displace(x0,y0)
        self.r2rs.displace(x0,y0)
        
        # intersections inside road 2
        self.i2ld=new_intersection()                 # road 2, left destroyer
        self.i2rd=new_intersection()                 # road 2, right destroyer
        self.i2rs=new_intersection()                 # road 2, right slip

        # hook these up
        self.i2ld.add_road_end(self.r2lo)
        self.i2rd.add_road_end(self.r2ro)
        self.i2rs.add_road_end(self.r2ri)
        self.i2rs.add_road_end(self.r2rs)
        self.i2rs.add_road_start(self.r2ro)

        # intersections feeding into road 2 are defined and connected at feeding road

        # roads entering ne
        self.r3rs=road_segment(65,15,15,15,2,20)
        self.r3ri=road_segment(215,10,65,10,2,20)
        self.r3ro=road_segment(65,10,15,10,2,20)
        self.r3ro.add_trafficlight()
        self.light_set_2.add_light(self.r3ro)
        self.r3li=road_segment(215,5,65,5,2,20)
        self.r3lo=road_segment(65,5,15,5,2,20)
        self.r3lo.add_trafficlight()
        self.light_set_2.add_light(self.r3lo)
        self.r3lt=road_segment(65,0,15,0,2,20)
        self.r3lt.add_trafficlight()
        self.light_set_2.add_light(self.r3lt)

        self.r3rs.displace(x0,y0)
        self.r3ri.displace(x0,y0)
        self.r3ro.displace(x0,y0)
        self.r3li.displace(x0,y0)
        self.r3lo.displace(x0,y0)
        self.r3lt.displace(x0,y0)

        
        # intersections inside road 3
        self.i3lc=new_intersection()
        self.i3rc=new_intersection()
        self.i3rs=new_intersection()
        self.i3lt=new_intersection()

        # hook these up
        self.i3lc.add_road_start(self.r3li)
        self.i3rc.add_road_start(self.r3ri)
        self.i3rs.add_road_end(self.r3ri)
        self.i3lt.add_road_end(self.r3li)
        self.i3rs.add_road_start(self.r3ro)
        self.i3lt.add_road_start(self.r3lo)
        self.i3rs.add_road_start(self.r3rs)
        self.i3lt.add_road_start(self.r3lt)

        # intersections connecting road 3 to other roads
        self.i32rsrs=new_intersection()
        self.i38rori=new_intersection()
        self.i38lolo=new_intersection()
        self.i36ltlori=new_intersection()

        # hook these up last
        
        # roads leaving se
        self.r4lo=road_segment(15,-5,215,-5,2,20)
        self.r4ri=road_segment(15,-10,65,-10,2,20)
        self.r4ro=road_segment(65,-10,215,-10,2,20)
        self.r4rs=road_segment(15,-15,65,-15,2,20)

        self.r4lo.displace(x0,y0)
        self.r4ri.displace(x0,y0)
        self.r4ro.displace(x0,y0)
        self.r4rs.displace(x0,y0)

        # intersections inside road 4
        self.i4ld=new_intersection()
        self.i4rd=new_intersection()
        self.i4rs=new_intersection()

        # hook these up
        self.i4ld.add_road_end(self.r4lo)
        self.i4rd.add_road_end(self.r4ro)
        self.i4rs.add_road_end(self.r4rs)
        self.i4rs.add_road_start(self.r4ro)
        self.i4rs.add_road_end(self.r4ri)

        # intersections feeding into this road are defined at intersecting road

        # roads entering se
        self.r5rs=road_segment(15,-65,15,-15,2,20)
        self.r5ri=road_segment(10,-215,10,-65,2,20)
        self.r5ro=road_segment(10,-65,10,-15,2,20)
        self.r5ro.add_trafficlight()
        self.light_set_1.add_light(self.r5ro)
        self.r5li=road_segment(5,-215,5,-65,2,20)
        self.r5lo=road_segment(5,-65,5,-15,2,20)
        self.r5lo.add_trafficlight()
        self.light_set_1.add_light(self.r5lo)
        self.r5lt=road_segment(0,-65,0,-15,2,20)
        self.r5lt.add_trafficlight()
        self.light_set_1.add_light(self.r5lt)

        self.r5rs.displace(x0,y0)
        self.r5ri.displace(x0,y0)
        self.r5ro.displace(x0,y0)
        self.r5li.displace(x0,y0)
        self.r5lo.displace(x0,y0)
        self.r5lt.displace(x0,y0)
        
        # intersections inside road 5
        self.i5rc=new_intersection()
        self.i5lc=new_intersection()
        self.i5rs=new_intersection()
        self.i5lt=new_intersection()

        # hook these up
        self.i5rc.add_road_start(self.r5ri)
        self.i5lc.add_road_start(self.r5li)
        self.i5rs.add_road_start(self.r5rs)
        self.i5rs.add_road_start(self.r5ro)
        self.i5rs.add_road_end(self.r5ri)
        self.i5lt.add_road_end(self.r5li)
        self.i5lt.add_road_start(self.r5lt)
        self.i5lt.add_road_start(self.r5lo)

        # intersections connecting road 5 to other roads

        self.i54rsrs=new_intersection()
        self.i52rori=new_intersection()
        self.i52lolo=new_intersection()
        self.i58ltlori=new_intersection()

        # hook these up last

        # roads leaving sw
        self.r6lo=road_segment(-5,-15,-5,-215,2,20)
        self.r6ri=road_segment(-10,-15,-10,-65,2,20)
        self.r6ro=road_segment(-10,-65,-10,-215,2,20)
        self.r6rs=road_segment(-15,-15,-15,-65,2,20)

        self.r6lo.displace(x0,y0)
        self.r6ri.displace(x0,y0)
        self.r6ro.displace(x0,y0)
        self.r6rs.displace(x0,y0)

        # intersections inside road 6
        self.i6rd=new_intersection()
        self.i6ld=new_intersection()
        self.i6rs=new_intersection()

        # hook these up
        self.i6rd.add_road_end(self.r6ro)
        self.i6ld.add_road_end(self.r6lo)
        self.i6rs.add_road_end(self.r6ri)
        self.i6rs.add_road_start(self.r6ro)
        self.i6rs.add_road_end(self.r6rs)

        # roads entering sw
        self.r7rs=road_segment(-65,-15,-15,-15,2,20)
        self.r7ri=road_segment(-215,-10,-65,-10,2,20)
        self.r7ro=road_segment(-65,-10,-15,-10,2,20)
        self.r7ro.add_trafficlight()
        self.light_set_2.add_light(self.r7ro)
        self.r7li=road_segment(-215,-5,-65,-5,2,20)
        self.r7lo=road_segment(-65,-5,-15,-5,2,20)
        self.r7lo.add_trafficlight()
        self.light_set_2.add_light(self.r7lo)
        self.r7lt=road_segment(-65,0,-15,0,2,20)
        self.r7lt.add_trafficlight()
        self.light_set_2.add_light(self.r7lt)

        self.r7rs.displace(x0,y0)
        self.r7ri.displace(x0,y0)
        self.r7ro.displace(x0,y0)
        self.r7li.displace(x0,y0)
        self.r7lo.displace(x0,y0)
        self.r7lt.displace(x0,y0)

        # intersections inside road 7
        self.i7rc=new_intersection()
        self.i7lc=new_intersection()
        self.i7rs=new_intersection()
        self.i7lt=new_intersection()

        # hook these up
        self.i7rc.add_road_start(self.r7ri)
        self.i7lc.add_road_start(self.r7li)
        self.i7rs.add_road_start(self.r7rs)
        self.i7rs.add_road_start(self.r7ro)
        self.i7rs.add_road_end(self.r7ri)
        self.i7lt.add_road_end(self.r7li)
        self.i7lt.add_road_start(self.r7lt)
        self.i7lt.add_road_start(self.r7lo)

        # intersections connecting road 7 to other roads
        self.i76rsrs=new_intersection()
        self.i74rori=new_intersection()
        self.i74lolo=new_intersection()
        self.i72ltlori=new_intersection()

        # hook these up last

        # roads leaving nw
        self.r8lo=road_segment(-15,5,-215,5,2,20)
        self.r8ri=road_segment(-15,10,-65,10,2,20)
        self.r8ro=road_segment(-65,10,-215,10,2,20)
        self.r8rs=road_segment(-15,15,-65,15,2,20)

        self.r8lo.displace(x0,y0)
        self.r8ri.displace(x0,y0)
        self.r8ro.displace(x0,y0)
        self.r8rs.displace(x0,y0)

        #intersections inside road 8
        self.i8ld=new_intersection()
        self.i8rd=new_intersection()
        self.i8rs=new_intersection()

        # hook these up
        self.i8ld.add_road_end(self.r8lo)
        self.i8rd.add_road_end(self.r8ro)
        self.i8rs.add_road_end(self.r8ri)
        self.i8rs.add_road_end(self.r8rs)
        self.i8rs.add_road_start(self.r8ro)

        #hook up all intersecting roads

        self.i18rsrs.add_road_end(self.r1rs)
        self.i18rsrs.add_road_start(self.r8rs)
        self.i16lolo.add_road_end(self.r1lo)
        self.i16lolo.add_road_start(self.r6lo)
        self.i16rori.add_road_end(self.r1ro)
        self.i16rori.add_road_start(self.r6ri)
        self.i14ltlori.add_road_end(self.r1lt)
        self.i14ltlori.add_road_start(self.r4lo)
        self.i14ltlori.add_road_start(self.r4ri)

        self.i32rsrs.add_road_end(self.r3rs)
        self.i32rsrs.add_road_start(self.r2rs)
        self.i38rori.add_road_end(self.r3ro)
        self.i38rori.add_road_start(self.r8ri)
        self.i38lolo.add_road_end(self.r3lo)
        self.i38lolo.add_road_start(self.r8lo)
        self.i36ltlori.add_road_end(self.r3lt)
        self.i36ltlori.add_road_start(self.r6lo)
        self.i36ltlori.add_road_start(self.r6ri)

        self.i54rsrs.add_road_end(self.r5rs)
        self.i54rsrs.add_road_start(self.r4rs)
        self.i52rori.add_road_end(self.r5ro)
        self.i52rori.add_road_start(self.r2ri)
        self.i52lolo.add_road_end(self.r5lo)
        self.i52lolo.add_road_start(self.r2lo)
        self.i58ltlori.add_road_end(self.r5lt)
        self.i58ltlori.add_road_start(self.r8lo)
        self.i58ltlori.add_road_start(self.r8ri)

        self.i76rsrs.add_road_end(self.r7rs)
        self.i76rsrs.add_road_start(self.r6rs)
        self.i74rori.add_road_end(self.r7ro)
        self.i74rori.add_road_start(self.r4ri)
        self.i74lolo.add_road_end(self.r7lo)
        self.i74lolo.add_road_start(self.r4lo)
        self.i72ltlori.add_road_end(self.r7lt)
        self.i72ltlori.add_road_start(self.r2lo)
        self.i72ltlori.add_road_start(self.r2ri)

        # add oncoming lanes
        self.r1lt.add_oncoming(self.r5lo)
        self.r1lt.add_oncoming(self.r5ro)
        self.r5lt.add_oncoming(self.r1lo)
        self.r5lt.add_oncoming(self.r1ro)
        self.r3lt.add_oncoming(self.r7lo)
        self.r3lt.add_oncoming(self.r7ro)
        self.r7lt.add_oncoming(self.r3lo)
        self.r7lt.add_oncoming(self.r3ro)

        self.add_to_world(w)

    def add_to_world(self,w):

        w.add_road_segment(self.r1rs)
        w.add_road_segment(self.r1ri)
        w.add_road_segment(self.r1ro)
        w.add_road_segment(self.r1li)
        w.add_road_segment(self.r1lo)
        w.add_road_segment(self.r1lt)
        w.add_road_segment(self.r3rs)
        w.add_road_segment(self.r3ri)
        w.add_road_segment(self.r3ro)
        w.add_road_segment(self.r3li)
        w.add_road_segment(self.r3lo)
        w.add_road_segment(self.r3lt)
        w.add_road_segment(self.r5rs)
        w.add_road_segment(self.r5ri)
        w.add_road_segment(self.r5ro)
        w.add_road_segment(self.r5li)
        w.add_road_segment(self.r5lo)
        w.add_road_segment(self.r5lt)
        w.add_road_segment(self.r7rs)
        w.add_road_segment(self.r7ri)
        w.add_road_segment(self.r7ro)
        w.add_road_segment(self.r7li)
        w.add_road_segment(self.r7lo)
        w.add_road_segment(self.r7lt)
        w.add_road_segment(self.r2rs)
        w.add_road_segment(self.r2ri)
        w.add_road_segment(self.r2ro)
        w.add_road_segment(self.r2lo)
        w.add_road_segment(self.r4rs)
        w.add_road_segment(self.r4ri)
        w.add_road_segment(self.r4ro)
        w.add_road_segment(self.r4lo)
        w.add_road_segment(self.r6rs)
        w.add_road_segment(self.r6ri)
        w.add_road_segment(self.r6ro)
        w.add_road_segment(self.r6lo)
        w.add_road_segment(self.r8rs)
        w.add_road_segment(self.r8ri)
        w.add_road_segment(self.r8ro)
        w.add_road_segment(self.r8lo)

        w.add_intersection(self.i1rc)
        w.add_intersection(self.i1lc)
        w.add_intersection(self.i1rs)
        w.add_intersection(self.i1lt)
        w.add_intersection(self.i3rc)
        w.add_intersection(self.i3lc)
        w.add_intersection(self.i3rs)
        w.add_intersection(self.i3lt)
        w.add_intersection(self.i5rc)
        w.add_intersection(self.i5lc)
        w.add_intersection(self.i5rs)
        w.add_intersection(self.i5lt)
        w.add_intersection(self.i7rc)
        w.add_intersection(self.i7lc)
        w.add_intersection(self.i7rs)
        w.add_intersection(self.i7lt)
        w.add_intersection(self.i2rd)
        w.add_intersection(self.i2ld)
        w.add_intersection(self.i2rs)
        w.add_intersection(self.i4rd)
        w.add_intersection(self.i4ld)
        w.add_intersection(self.i4rs)
        w.add_intersection(self.i6rs)
        w.add_intersection(self.i6rd)
        w.add_intersection(self.i6ld)
        w.add_intersection(self.i8rd)
        w.add_intersection(self.i8rs)
        w.add_intersection(self.i8ld)
        w.add_intersection(self.i18rsrs)
        w.add_intersection(self.i16rori)
        w.add_intersection(self.i16lolo)
        w.add_intersection(self.i14ltlori)
        w.add_intersection(self.i32rsrs)
        w.add_intersection(self.i38rori)
        w.add_intersection(self.i38lolo)
        w.add_intersection(self.i36ltlori)
        w.add_intersection(self.i54rsrs)
        w.add_intersection(self.i52rori)
        w.add_intersection(self.i52lolo)
        w.add_intersection(self.i58ltlori)
        w.add_intersection(self.i76rsrs)
        w.add_intersection(self.i74rori)
        w.add_intersection(self.i74lolo)
        w.add_intersection(self.i72ltlori)
