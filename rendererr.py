from ursina import *   
from asterion import *
import random
seed=random.randint(0,10000000)
system=generate_system(seed)
simulation_speed=10
simulation_elapsed=0
positions=current_position(system,simulation_elapsed)
app=Ursina()
window.color=color.black
visual_star=Entity(model='sphere',color=color.yellow,scale=(3,3,3),position=(0,0,0))


def create_planets(positions):
    visual_planet=[]
    for i in positions:
        visual_planet.append(Entity(model='sphere',color=color.blue,scale=(1,1,1),position=(i[0]*10,0,i[1]*10)))        
    return visual_planet

def create_orbits(system):
    orbit=[]
    for i in range(len(system.planets)):
        orbit.append(Entity(model=Circle(mode='line',resolution=100,radius=system.planets[i].orbital_distance*10),color=color.white,position=(0,0,0),rotation=(90,0,0)))
    return orbit
orbits=create_orbits(system)
visual_planet=create_planets(positions)

simulation_paused=False
def update():
    global simulation_elapsed
    if simulation_paused==False:
        simulation_elapsed+=time.dt*simulation_speed
        position=current_position(system,simulation_elapsed)
        for i in range(len(position)):
            visual_planet[i].position=(position[i][0]*10,0,position[i][1]*10)

def input(key):
    global seed
    global system
    global orbits
    global visual_planet
    global simulation_paused
    global simulation_speed
    global simulation_elapsed
    global text
    if key=='space':
        simulation_paused=not simulation_paused
    if key=='up arrow':
        simulation_speed+=1
    if key=='down arrow':
        if simulation_speed-1>0:
            simulation_speed-=1
        else:
            simulation_speed=1
    if key=='n':
        simulation_speed=1
        simulation_elapsed=0
        seed=random.randint(0,10000000)
        for i in visual_planet:
            destroy(i)
        for i in orbits:
            destroy(i)
        
        system=generate_system(seed)
        orbits=create_orbits(system)
        positions=current_position(system,simulation_elapsed)
        visual_planet=create_planets(positions)
        destroy(text)
        text=Text(text='PLANETARY SYSTEM\nSEED:{}\nSTAR MASS:{}\nPLANET COUNT:{}'.format(seed,system.star.mass,len(system.planets)),position=window.top_left)




EditorCamera(rotation_speed=200,zoom_speed=1.25)
text=Text(text='PLANETARY SYSTEM\nSEED:{}\nSTAR MASS:{}\nPLANET COUNT:{}'.format(seed,system.star.mass,len(system.planets)),position=window.top_left)

app.run()              
