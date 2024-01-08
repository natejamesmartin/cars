from random import randint
from random import seed
import numpy as np
from math import sqrt

import copy

seed(1)
np.random.seed(1)

color = ["red", "blue", "green", "gray", "purple", "orange"]

class car:
    def __init__(self,road,x=0,y=0,vi=10):
        self.vmax=np.random.poisson(lam=10, size=1)[0] # m/s
        # self.vmax=10 # m/s
        self.x=x # m
        self.y=y # m
        self.v=vi # m/s
        self.acceltime=5 # s
        self.road=road
        self.unitx=self.road.unitx
        self.unity=self.road.unity
        self.vx=self.v*self.unitx
        self.vy=self.v*self.unity
        
        #self.color=np.random.rand(1)[0]
        self.color=color[randint(0,len(color)-1)]

        self.a=(self.vmax-self.v)/self.acceltime # m/s^2
        self.ax=self.a*self.unitx
        self.ay=self.a*self.unity

        self.waiting=False
        self.free_to_merge=False

        self.assign_next_road()

    def assign_next_road(self):
        # selects the next road this car will go onto
        thisint=self.road.endint
        # find available road segments to go on to
        starts=thisint.road_starts
        # pick one and assign as next road segment
        if len(starts)>0:
            random_index=randint(0,len(starts)-1)
            newroad=starts[random_index]
            self.next_road=newroad
            self.next_road_listindex=random_index
        else:
            self.next_road_listindex=-1 # this intersection must be a destroyer

    def distance_to_end(self):
        d=self.road.length-self.distance_from_start()
        return d
    def distance_from_start(self):
        d=sqrt((self.road.startx-self.x)**2+(self.road.starty-self.y)**2)
        return d
    def update_road(self,newroad):
        # update everything related to the new road we got put on
        self.road=newroad
        self.unitx=self.road.unitx
        self.unity=self.road.unity
        self.vx=self.v*self.unitx
        self.vy=self.v*self.unity
        self.ax=self.a*self.unitx
        self.ay=self.a*self.unity
        self.waiting=False
        self.free_to_merge=False
        self.assign_next_road()

        
    def step(self, dt):
        self.v=self.v+self.a*dt
        if self.v>self.vmax:
            self.v=self.vmax
            self.a=0
        self.vx=self.v*self.unitx
        self.vy=self.v*self.unity
        self.x=self.x+self.vx*dt
        self.y=self.y+self.vy*dt
        
class carlist:
    def __init__(self,road):
        self.n=0
        self.road=road
        self.carlist=[]
        self.time_since_creation=0
        self.poisson_time_to_create=20 # s
        self.nextt=0 # try to create a new car at t=0
    def printcars(self):
        print (self.xs())
    def addcar(self,c):
        self.carlist.append(c)
        self.n+=1
    def addcarpos(self,x,y):
        c=car(self.road,x,y)
        self.addcar(c)
    def addcarstart(self):
        c=car(self.road,self.road.startx,self.road.starty)
        self.addcar(c)
    def step(self,dt):
        # go through and step each car forward
        for i,c in enumerate(self.carlist):
            c.step(dt)
        

        if len(self.carlist)>0:
            c=self.carlist[0]

            #Check to see if car is close to a traffic light
            if ((self.road.trafficlight)
                &((self.road.trafficlightcolor=='red')
                   |(self.road.trafficlightcolor=='yellow'))):
                if c.distance_to_end()<10:
                    c.v=0 # m/s
                    c.a=0 # m/s2
                    #c.waiting=True
                elif (c.distance_to_end()<50) & (c.v>0):
                    c.a=-1 # m/s2

            # Check to see if car is close to a stop sign
            if (self.road.stopsign) & (c.free_to_merge==False):
                if c.distance_to_end()<10:
                    c.v=0 # m/s
                    c.a=0 # m/s2
                    c.waiting=True
                elif (c.distance_to_end()<50) & (c.v>0):
                    c.a=-1 # m/s2

                # Make car move again
                if c.waiting:
                    # Look to see if a car is coming
                    car_coming=False
                    thisint=self.road.endint
                    ends=thisint.road_ends
                    for end in ends:
                        must_yield=False
                        if not end.stopsign:
                            yieldto=end
                            must_yield=True
                        if must_yield:
                            closestdistance=yieldto.length
                            if len(yieldto.carlist.carlist)>0:
                                closestdistance=yieldto.carlist.carlist[0].distance_to_end()
                            if closestdistance<100:
                                car_coming=True

                    # Look to see if a car is ahead
                    car_ahead=True
                    starts=thisint.road_starts
                    if(len(starts)>0):
                        start=starts[0]
                        closestdistance_ahead=start.length
                        if len(start.carlist.carlist)>0:
                            closestdistance_ahead=start.carlist.carlist[-1].distance_from_start()
                        if closestdistance_ahead>10:
                            car_ahead=False

                    if (not car_coming) and (not car_ahead):
                        c.free_to_merge=True
                        c.waiting=False


            # Check to see if car made it to the end of the road
            # segment.  Look at carlist[0] to see if this car has
            # reached the end of this road and either delete it or
            # move it to the next road.
            
            if c.distance_to_end()<0:
                print("the car reached the end of the road segment")
                # find the intersection at the end of this road
                thisint=self.road.endint
                # find available road segments to go on to
                starts=thisint.road_starts
                # pick one and move the car to that road segment
                if len(starts)>0:
                    newroad=starts[randint(0,len(starts)-1)]
                    print("Moving car from",self.road.id,"to",newroad.id)
                    # newroad.carlist.carlist.append(copy.deepcopy(c))
                    # not sure if we need to copy it, or not
                    # let's try without, at first
                    newroad.carlist.carlist.append(c)
                    newroad.carlist.carlist[-1].x=newroad.startx
                    newroad.carlist.carlist[-1].y=newroad.starty
                    newroad.carlist.carlist[-1].update_road(newroad)
                # or do nothing if the intersection is a destroyer
                del self.carlist[0]

        # modify speeds and accelerations to avoid collisions
        for i,ci in enumerate(self.carlist):
            # find the closest car in front of me
            closestindex=i-1
            if closestindex!=-1:
                closestcar=self.carlist[closestindex]
                closestdistance=self.distance(ci,closestcar)
                #print("the closest car to car ",i, "is", closestindex)

                if (closestdistance<10):
                    ci.v=0 # m/s
                    ci.a=0 # m/s2
                    #print("close avoidance",i,closestindex,self.xs())
                elif (closestdistance<50) & (ci.v>0):
                    ci.a=-1 # m/s2
                    #print("collision avoidance",i,closestindex,self.xs())
                elif ci.v<ci.vmax:
                    ci.a=1
                else:
                    ci.a=0
            else: # car is at the front of the line
                if ci.v<ci.vmax:
                    if ci.waiting==False:
                        ci.a=1
                    else:
                        ci.a=0
                else:
                    ci.a=0

        # if the intersection at the start of this road is a creator,
        # consider making a car
        if self.road.startint.is_creator():
            #print("Checking to see if we should create a car on",self.road.id)
            self.time_since_creation+=dt
            if (self.time_since_creation>self.nextt):

                # find the car closest to start and make sure it's far away
                create_car=False
                if len(self.carlist)>0:
                    c=self.carlist[-1]
                    if c.distance_from_start()>50:
                        create_car=True
                        print("There are cars already, and we should make a new one.")
                else:
                    create_car=True
                    print("No cars, here!  Let us make one!")

                if create_car:
                    print("creating car")
                    self.addcarstart()
                    # decide how long to wait before creating next car
                    self.nextt=np.random.poisson(lam=self.poisson_time_to_create,size=1)[0]
                    self.nextt+=1 # make sure it can't be zero
                    print("Next car will be created in about",self.nextt,"s")
                    self.time_since_creation=0 # reset the clock

    def distance(self,car1,car2):
        d=sqrt((car1.x-car2.x)**2+(car1.y-car2.y)**2)
        return d
    def xs(self):
        l=[]
        for c in self.carlist:
            l.append(c.x)
        return l
    def ys(self):
        l=[]
        for c in self.carlist:
            l.append(c.y)
        return l
    def colors(self):
        l=[]
        for c in self.carlist:
            l.append(c.color)
        return l
    def initialize(self,ncars):
        poslist=[]
        for i in range(ncars):
            pos=np.random.rand(1)[0]*self.road.length
            poslist.append(pos)
        poslist.sort(reverse=True)
        print(poslist)
        for pos in poslist:
            x=self.road.startx+pos*self.road.unitx
            y=self.road.starty+pos*self.road.unity
            self.addcarpos(x,y)
