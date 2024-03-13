from math import sqrt
import itertools
from carlist import carlist
from carlist import car
import matplotlib.pyplot as plt
import parameters

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
        print("initializing intersection number",self.id,tietogether)
        self.cycletime=0
        for tiethese in tietogether:
            print("tie the following traffic lights together")
            for seg in tiethese:
                print(seg.id)
        self.trafficlights=tietogether
        if len(self.trafficlights)==0:
            for seg in self.road_ends:
                if seg.trafficlight:
                    self.trafficlights.append([seg])
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
    def printstats(self):
        with open('road_stats.out','w') as f:
            f.write("integer creationtime deletiontime lifetime\n")
        for seg in self.road_segments:
            i=seg.endint
            if i.is_destroyer():                
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
                print("This intersection is at x=%f y=%f"%(i.x(),i.y()))
                lifetimes=[]
                cs=seg.carlist.cs
                for i,ct in enumerate(cs.creationtimes):
                    lifetimes.append(cs.deletiontimes[i]-cs.creationtimes[i])
                plt.scatter(cs.creationtimes,lifetimes)
        plt.xlabel('creation time (s)')
        plt.ylabel('lifetime (s)')
        plt.savefig('lt-vs-ct.png')
