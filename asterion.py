import random
import math



class Star:
    def __init__(self,mass,luminosity,temperature):
        self.mass=mass
        self.luminosity=luminosity
        self.temperature=temperature



class Planet:
    def __init__(self,mass,orbital_distance,starting_angle,spin_speed):
        self.mass=mass
        self.orbital_distance=orbital_distance
        self.starting_angle=starting_angle
        self.spin_speed=spin_speed




class System:
    def __init__(self,planets,star):
        self.planets=planets
        self.star=star



def generate_system(seed):
    random.seed(seed)
    star_mass=random.uniform(0.3,3.0)
    star_luminosity=star_mass**4
    star_temperature=star_mass**0.6
    star=Star(star_mass,star_luminosity,star_temperature)
    planet_no=random.randint(2,8)
    l=[]
    j,k=0.5,1
    for i in range(planet_no):
        planet_mass=random.uniform(0.5,5)
        planet_distance=random.uniform(j,k)
        planet_angle=random.uniform(0,360)
        planet_spin_speed=random.uniform(8,30)
        planet=Planet(planet_mass,planet_distance,planet_angle,planet_spin_speed)
        l.append(planet)
        j=j+1
        k=k+1
    system=System(l,star)
    return system

def current_position(oursystem,elapsed_time):
    
    d=[]
    for i in oursystem.planets:
        d.append(i.orbital_distance)
    t=[]
    for i in range(len(d)):
        t.append((math.sqrt((d[i])**3/oursystem.star.mass))*365.25)
    
    current_angle=[]
    for i in range(len(t)):
        fraction=elapsed_time/t[i]
        if fraction>1:
            fraction=fraction-int(fraction)
        current_angle.append((oursystem.planets[i].starting_angle+(360*fraction))%360)
    for i in range(len(current_angle)):
        current_angle[i]=math.radians(current_angle[i])
    position=[]
    for i in range(len(current_angle)):
        position.append([oursystem.planets[i].orbital_distance*math.cos(current_angle[i]),oursystem.planets[i].orbital_distance*math.sin(current_angle[i])])
    return position





