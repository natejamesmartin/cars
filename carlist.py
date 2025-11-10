from math import acos
from random import randint
from random import seed
import numpy as np
from math import sqrt
from math import pi
import parameters
import copy
from CLVars import parse_my_args
import CLVars
import argparse
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

args = parse_my_args()


seed(parameters.seed)
np.random.seed(parameters.seed)

dt = 0.1 # s

color = ["red","blue","green","gray","purple","orange"]

g = 9.8 # m/s**2
mu_r = 0.012 # coef of friction for a standard car
cda = 0.654 # m**2; coef of drag * frontal area of car
rho = 1.21 # kg/m**3; density of air
displacement = 1.7 # L; engine displacement of a 2005 Honda Civic
idling = 0.6 # L/h/L of engine displacement
ic = idling*displacement/3600 # L/s; idling consumption
h = 34000000 # J/L; enthalpy of combustion of gasoline
epsilon = 0.2 # engine efficiency

# https://c21.phas.ubc.ca/article/energy-use-in-vehicles/
# https://oee.nrcan.gc.ca/transportation/idling/calculations.cfm?attr-28

class car:
    number = 0
    def __init__(self,road,x=0,y=0,t=0,vi=10,m=1000):
        self.vmax=np.random.poisson(lam=parameters.poisson_vmax, size=1)[0] # m/s
        if self.vmax==0:  # don't allow cars with zero speed
            self.vmax=1
        # self.vmax=10 # m/s
        self.x=x # m
        self.y=y # m
        self.v=self.vmax # m/s
        self.acceltime=5 # s
        self.road=road
        self.unitx=self.road.unitx
        self.unity=self.road.unity
        self.vx=self.v*self.unitx
        self.vy=self.v*self.unity
        self.time = 0
        
        #self.color=np.random.rand(1)[0]

        self.carnum = car.number
        
        car.number+=1

        self.color=color[randint(0,len(color)-1)]
        if(self.carnum == args.carnum):
            self.color = 'pink'
        
        self.a=(self.vmax-self.v)/self.acceltime # m/s^2
        self.ax=self.a*self.unitx
        self.ay=self.a*self.unity

        self.waiting=False
        self.free_to_merge=False

        self.assign_next_road()

        self.creationtime=t

        self.carinfo = randint(0,2)
        if(self.carinfo == 1):
            #fuel efficient
            self.m=m # kg
        if(self.carinfo==2):
            #normal
            self.m=m #kg
        if(self.carinfo==0):
            #gas guzzler
            self.m=m #kg
        

        self.ke = 0.5*self.m*self.v**2 # J
        self.fa = 0.5*rho*cda*self.v**2 # N; air drag force
        self.fr = self.m*g*mu_r # N; rotational friction force
        self.pmech = self.v*(self.fr+self.fa) # W

        self.fuel = 0 # L of fuel consumed

    def assign_next_road(self):
        # selects the next road this car will go onto
        thisint=self.road.endint
        # find available road segments to go on to
        starts=thisint.road_starts
        # pick one and assign as next road segment
        if len(starts)>0:
            while True:
                random_index=randint(0,len(starts)-1)
                newroad=starts[random_index]
                self.next_turn=self.findangle(self.road,newroad)
                if(self.next_turn!='u-turn'): # to get rid of u-turns
                    #if(self.next_turn=='left'): # to force all left turns
                    break
            self.next_road=newroad
            self.next_road_listindex=random_index
            if(args.verbose==1):
                print("this car is on road number",self.road.id,"and it is turning on to",self.next_road.id)
                print("The",self.color,"car will go",self.next_turn)
        else:
            self.next_road_listindex=-1 # this intersection must be a destroyer
            self.next_turn='none'

    def findangle(self,road1,road2):
        deltax1=road1.endx-road1.startx
        deltay1=road1.endy-road1.starty
        deltax2=road2.endx-road2.startx
        deltay2=road2.endy-road2.starty
        dotproduct=deltax1*deltax2+deltay1*deltay2
        crossproduct=deltax1*deltay2-deltay1*deltax2
        costheta=dotproduct/(sqrt(deltax1**2+deltay1**2)*sqrt(deltax2**2+deltay2**2))
        angle=acos(costheta)*180/pi
        precision=0.001
        if(abs(costheta-1)<precision): # costheta=1 means theta=0
            value='straight'
        elif(abs(costheta+1)<precision): # costheta=-1 means theta=180 deg
            value='u-turn'
        else: # must be a left turn or a right turn
            if(crossproduct>0):
                value='left'
            else:
                value='right'
        return value
            
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
        self.time += dt
        pmechi = self.pmech
        kei = self.ke
        self.v=self.v+self.a*dt
        if self.v>self.vmax:
            self.v=self.vmax
            self.a=0
        self.vx=self.v*self.unitx
        self.vy=self.v*self.unity
        self.x=self.x+self.vx*dt
        self.y=self.y+self.vy*dt
        self.update_energy()
        kef = self.ke
        dke = kef-kei
        if(dke==0 and self.ke==0):
            dw = ic*dt*epsilon*h # J
            print('Idling',self.carnum,dw)
        elif(dke >= 0):
            dw = dke + pmechi*dt # J
            print('Cruising or accelerating',self.carnum,dw)
        else: # dke < 0
            dw = ic*dt*epsilon*h # J
            print('Decelerating',self.carnum,dw)
        dfuel = dw/epsilon/h
        self.fuel += dfuel
        if(self.carnum == args.carnum):
            print('Car Number ',self.carnum,':')
            print('KE_i = ',kei)
            print('KE_f = ',kef)
            print('pmechi = ',pmechi)
            print('pmechf = ',self.pmech)
            print('frf = ',self.fr)
            print('faf = ',self.fa)
            print('Fuel = ',self.fuel)
            print('Speed = ',self.v)
            print('Time = ',self.time)
            time.sleep(0.1)

            #xFuel.append(self.time)
            #yFuel.append(self.fuel)
    def update_energy(self):
        self.ke = 0.5*self.m*self.v**2 # J
        self.fa = 0.5*rho*cda*self.v**2 # N; air drag force
        self.fr = self.m*g*mu_r # N; rotational friction force
        self.pmech = self.v*(self.fr+self.fa) # W

class carstats:
    def __init__(self):
        self.carnums=[]
        self.creationtimes=[]
        self.deletiontimes=[]
        self.fuels=[]
    def savetimes(self,carnum,creationtime,deletiontime):
        self.carnums.append(carnum)
        self.creationtimes.append(creationtime)
        self.deletiontimes.append(deletiontime)
    def savefuel(self,fuel):
        self.fuels.append(fuel)
    def printstats(self):
        print(self.carnums)
        print(self.creationtimes)
        print(self.deletiontimes)
        print(self.fuels)
        
class carlist:
    def __init__(self,road):
        self.n=0
        self.road=road
        self.carlist=[]
        self.time_since_creation=0
        self.poisson_time_to_create=parameters.poisson_time_to_create # s
        self.nextt=0 # try to create a new car at t=0
        self.t=0
        self.cs=carstats()
    def printcars(self):
        print (self.xs())
    def addcar(self,c):
        self.carlist.append(c)
        self.n+=1
    def addcarpos(self,x,y):
        c=car(self.road,x,y,self.t)
        self.addcar(c)
    def addcarstart(self):
        c=car(self.road,self.road.startx,self.road.starty,self.t)
        self.addcar(c)
    def step(self,dt):
        # go through and step each car forward
        for i,c in enumerate(self.carlist):
            c.step(dt)

        self.t+=dt
        
        if len(self.carlist)>0:
            # Check for things to do with the first car on this road segment
            c=self.carlist[0]

            # Don't wait if we're at a green light
            if ((self.road.trafficlight)
                &(self.road.trafficlightcolor=='green')):
                c.waiting=False
            
            #Check to see if car is close to a red traffic light
            if ((self.road.trafficlight)
                &(self.road.trafficlightcolor=='red')):
                if c.distance_to_end()<parameters.stopdistance:
                    c.v=0 # m/s
                    c.a=0 # m/s2
                    c.waiting=True
                elif (c.distance_to_end()<parameters.brakedistance) & (c.v>0):
                    c.a=-1 # m/s2
                    c.waiting=False
                else:
                    c.waiting=False

            #Check to see if car is close to a yellow traffic light
            if ((self.road.trafficlight)
                &(self.road.trafficlightcolor=='yellow')
                &((c.next_turn!='left') | (parameters.lt_yellow==False))):
                if c.distance_to_end()<parameters.stopdistance:
                    c.v=0 # m/s
                    c.a=0 # m/s2
                    c.waiting=True
                elif (c.distance_to_end()<parameters.brakedistance) & (c.v>0):
                    c.a=-1 # m/s
                    c.waiting=False
                else:
                    c.waiting=False

            # Check to see if car is close to a stop sign
            if (self.road.stopsign) & (c.free_to_merge==False):
                if c.distance_to_end()<parameters.stopdistance:
                    c.v=0 # m/s
                    c.a=0 # m/s2
                    c.waiting=True
                elif (c.distance_to_end()<parameters.brakedistance) & (c.v>0):
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
                            if closestdistance<parameters.mergedistance:
                                car_coming=True

                    # Look to see if a car is ahead
                    car_ahead=True
                    starts=thisint.road_starts
                    if(len(starts)>0):
                        start=starts[0]
                        closestdistance_ahead=start.length
                        if len(start.carlist.carlist)>0:
                            closestdistance_ahead=start.carlist.carlist[-1].distance_from_start()
                        if closestdistance_ahead>parameters.stopdistance:
                            car_ahead=False

                    if (not car_coming) and (not car_ahead):
                        c.free_to_merge=True
                        c.waiting=False


            # Check to see if car made it to the end of the road
            # segment.  Look at carlist[0] to see if this car has
            # reached the end of this road and either delete it or
            # move it to the next road.
            
            if c.distance_to_end()<0:
                if(args.verbose == 1):
                    print("the car reached the end of the road segment")
                # find the intersection at the end of this road
                thisint=self.road.endint
                # find available road segments to go on to
                starts=thisint.road_starts
                # pick one and move the car to that road segment
                if len(starts)>0:
                    #newroad=starts[randint(0,len(starts)-1)]
                    newroad=c.next_road
                    if(args.verbose==1):
                        print("Moving car from",self.road.id,"to",newroad.id)
                    # newroad.carlist.carlist.append(copy.deepcopy(c))
                    # not sure if we need to copy it, or not
                    # let's try without, at first
                    newroad.carlist.carlist.append(c)
                    newroad.carlist.carlist[-1].x=newroad.startx
                    newroad.carlist.carlist[-1].y=newroad.starty
                    newroad.carlist.carlist[-1].update_road(newroad)
                else:
                    # or do nothing if the intersection is a destroyer
                    if(args.verbose==1):
                        print("%s car created at %f s deleted at %f s"%(c.color,c.creationtime,self.t))
                    self.cs.savetimes(c.carnum,c.creationtime,self.t)
                    self.cs.savefuel(c.fuel)
                del self.carlist[0]


        # Now look at all the cars.
        # Modify speeds and accelerations to avoid collisions.
        for i,ci in enumerate(self.carlist):
            # find the closest car in front of me
            closestindex=i-1
            if closestindex!=-1: # not the car at the front of the line
                closestcar=self.carlist[closestindex]
                closestdistance=self.distance(ci,closestcar)
                if(args.verbose==1):
                    print("the closest car to car ",i, "is", closestindex)

                if (closestdistance<parameters.stopdistance):
                    ci.v=0 # m/s
                    ci.a=0 # m/s2
                    if(args.verbose==1):
                        print("close avoidance",i,closestindex,self.xs())
                elif (closestdistance<parameters.brakedistance) & (ci.v>1):
                    ci.a=-1 # m/s2
                    if(args.verbose==1):
                        print("collision avoidance",i,closestindex,self.xs())
                elif ci.v<ci.vmax:
                    ci.a=1
                else:
                    ci.a=0
            else: # car is at the front of the line
                # we are coming up to the next road segment
                # search for the last car on the next road segment
                # make sure we don't run into it!
                if ci.next_road_listindex!=-1:
                    nextroad=ci.next_road
                    if len(ci.next_road.carlist.carlist)>0:
                        nextcar=ci.next_road.carlist.carlist[-1]
                        distance_to_nextcar=ci.distance_to_end()+nextcar.distance_from_start()
                    else:
                        distance_to_nextcar=ci.distance_to_end()+ci.next_road.length
                else:
                    distance_to_nextcar=200
                # Now we know the minimum distance to the next car in
                # front of us.  Make sure we slow down if we're
                # getting close.  Otherwise, either keep on going, or
                # go ahead and speed up again if traffic lights
                # permit.
                if (distance_to_nextcar<parameters.stopdistance):
                    ci.v=0 # m/s
                    ci.a=0 # m/s2
                    if(args.verbose==1):
                        print("close avoidance",i,closestindex,self.xs())
                elif (distance_to_nextcar<parameters.brakedistance) & (ci.v>1):
                    ci.a=-1 # m/s2
                    if(args.verbose==1):
                        print("collision avoidance",i,closestindex,self.xs())
                elif ci.v<ci.vmax:
                    if ci.waiting:
                        ci.a=0
                        ci.v=0
                    else:
                        ci.a=1
                else:
                    ci.a=0

                # If we're making a left turn, check for oncoming
                # traffic
                no_oncoming=True
                if ((ci.next_turn=='left')
                    & (len(self.road.oncoming)>0)
                    & (ci.distance_to_end()<parameters.brakedistance)):
                    for oncoming_road in self.road.oncoming:
                        if len(oncoming_road.carlist.carlist)>0:
                            oncoming_car=oncoming_road.carlist.carlist[0]
                            if ((oncoming_car.distance_to_end()<parameters.mergedistance)
                                & (oncoming_car.next_turn!='left')):
                                no_oncoming=False
                if ((ci.next_turn=='left')
                    & (parameters.lt_yellow==True)
                    & (self.road.trafficlightcolor=='yellow')):
                    no_oncoming=True
                if no_oncoming==False:
                    if (ci.distance_to_end()<parameters.stopdistance):
                        ci.v=0 # m/s
                        ci.a=0 # m/s2
                    elif (ci.distance_to_end()<parameters.mergedistance) & (ci.v>0):
                        ci.a=-1 # m/s2
                    else:
                        ci.a=1

        # if the intersection at the start of this road is a creator,
        # consider making a car
        if self.road.startint.is_creator():
            if(args.verbose==1):
                print("Checking to see if we should create a car on",self.road.id)
            self.time_since_creation+=dt
            if (self.time_since_creation>self.nextt):

                # find the car closest to start and make sure it's far away
                create_car=False
                if len(self.carlist)>0:
                    c=self.carlist[-1]
                    if c.distance_from_start()>parameters.brakedistance:
                        create_car=True
                        if(args.verbose==1):
                            print("There are cars already, and we should make a new one.")
                else:
                    create_car=True
                    #print("No cars, here!  Let us make one!")

                if create_car:
                    if(args.verbose==1):
                        print("creating car")
                    self.addcarstart()
                    # decide how long to wait before creating next car
                    self.nextt=np.random.poisson(lam=self.poisson_time_to_create,size=1)[0]
                    self.nextt+=1 # make sure it can't be zero
                    if(args.verbose==1):
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
        if(args.verbose==1):
            print(poslist)
        for pos in poslist:
            x=self.road.startx+pos*self.road.unitx
            y=self.road.starty+pos*self.road.unity
            self.addcarpos(x,y)

