from ursina import *   
from asterion import *
from PIL import Image,ImageDraw
import random
from pathlib import Path
seed=random.randint(0,10000000)
system=generate_system(seed)
simulation_speed=10
simulation_elapsed=0
positions=current_position(system,simulation_elapsed)
app=Ursina()
window.color=color.black
def create_main_star(system):
    visual_star=Entity(model='sphere',color=color.yellow,scale=((system.star.mass)**0.8*3,(system.star.mass)**0.8*3,(system.star.mass)**0.8*3),position=(0,0,0))
    return visual_star

def create_background_stars(seed):
    stars=[]
    for i in range(100):
        x=random.uniform(-1,1)
        y=random.uniform(-1,1)
        z=random.uniform(-1,1)
        length=300/((x**2+y**2+z**2)**0.5)
    
        stars.append(Entity(model='sphere',color=color.white,scale=(0.5,0.5,0.5),position=(x*length,y*length,z*length)))
    return stars    


def create_planets(positions):
    visual_planet=[]
    path=Path('textures/planets')
    texture_jpg=list(path.glob('*.jpg'))
    texture_png=list(path.glob('*.png'))
    texture_list=texture_jpg+texture_png
    
    for i in positions:
                
        l=random.choice(texture_list)
        blank_texture=Texture(l)
        visual_planet.append(Entity(model='sphere',color=color.white,scale=(system.planets[positions.index(i)].mass**0.27,system.planets[positions.index(i)].mass**0.27,system.planets[positions.index(i)].mass**0.27),position=(i[0]*10,0,i[1]*10),texture=blank_texture))
        texture_list.remove(l)   
    return visual_planet

def create_orbits(system):
    orbit=[]
    for i in range(len(system.planets)):
        orbit.append(Entity(model=Circle(mode='line',resolution=100,radius=system.planets[i].orbital_distance*10),color=color.white,position=(0,0,0),rotation=(90,0,0)))
    return orbit
star=create_main_star(system)
orbits=create_orbits(system)
visual_planet=create_planets(positions)
background_stars=create_background_stars(seed)

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
    global background_stars
    global star
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
        for i in background_stars:
            destroy(i)
        destroy(star)
        
        system=generate_system(seed)
        star=create_main_star(system)
        orbits=create_orbits(system)
        positions=current_position(system,simulation_elapsed)
        visual_planet=create_planets(positions)
        background_stars=create_background_stars(seed)
        destroy(text)
        text=Text(text='PLANETARY SYSTEM\nSEED:{}\nSTAR MASS:{}\nPLANET COUNT:{}'.format(seed,system.star.mass,len(system.planets)),position=window.top_left)




EditorCamera(rotation_speed=200,zoom_speed=1.25)
text=Text(text='PLANETARY SYSTEM\nSEED:{}\nSTAR MASS:{}\nPLANET COUNT:{}'.format(seed,system.star.mass,len(system.planets)),position=window.top_left)

app.run()              
