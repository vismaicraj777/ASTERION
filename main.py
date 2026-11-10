from ursina import *   
from asterion import *
from PIL import Image,ImageDraw
import random
from pathlib import Path

app=Ursina(window_title='ASTERION')
text1=Text(text='ASTERION',position=(-0.2,0.35,0),parent=camera.ui,scale=(3,3,3))
seed_field=InputField(text='',position=(0,0.1,0),limit_content_to='0123456789',color=color.white)
sky=Sky(texture="textures/background/7.png")

system=None

simulation_paused=False
def update():
    global simulation_elapsed
    if system!=None:
        if simulation_paused==False:
            simulation_elapsed+=time.dt*simulation_speed
            position=current_position(system,simulation_elapsed)
            for i in range(len(position)):
                visual_planet[i].position=(position[i][0]*10,0,position[i][1]*10)
                visual_planet[i].rotation_y+=system.planets[i].spin_speed*simulation_speed*time.dt
    else:
        return


def button_click():
    global seed
    global system
    global orbits
    global visual_planet
    global simulation_paused
    global simulation_speed
    global simulation_elapsed
    global text
    global sky
    global star
    simulation_elapsed=0
    simulation_speed=10
    if seed_field.text=='':
        seed=random.randint(0,10000000)
        destroy(sky)
        
    else:
        seed=int(seed_field.text)
        destroy(sky)
    system=generate_system(seed)
    
    positions=current_position(system,simulation_elapsed)
    sky=create_sky(seed)
    star=create_main_star(system)
    orbits=create_orbits(system)
    visual_planet=create_planets(positions,seed)
    text=Text(text='PLANETARY SYSTEM\nSEED:{}\nSTAR MASS(SM):{}\nPLANET COUNT:{}'.format(seed,system.star.mass,len(system.planets)),position=window.top_left)
    button.enabled=False
    text1.enabled=False
    seed_field.enabled=False


button=Button(text='CREATE PLANETARY SYSTEM',text_color=color.black,position=(0,0,0),parent=camera.ui,scale=(0.5,0.05,0.05),on_click=button_click,color=color.white)




window.color=color.black
def create_main_star(system):
    
    if system.star.temperature <= 0.64:
        blank_texture=Texture('textures/stars/red.jpeg')
    elif 0.64<system.star.temperature<=0.90:
        blank_texture=Texture('textures/stars/orange.jpg')
    elif 0.90<system.star.temperature<=1.03:
        blank_texture=Texture('textures/stars/yellow.jpeg')
    elif 1.03<system.star.temperature<=1.72:
        blank_texture=Texture('textures/stars/white.jpeg')
    else:
        blank_texture=Texture('textures/stars/blue.jpeg')



    

    visual_star=Entity(model='sphere',color=color.white,scale=((system.star.mass)**0.8*3,(system.star.mass)**0.8*3,(system.star.mass)**0.8*3),position=(0,0,0),texture=blank_texture)
    return visual_star

def create_sky(seed):
    sky_rng=random.Random(seed)
    path=Path('textures/background')
    texture_jpg=list(path.glob('*.jpg'))
    texture_png=list(path.glob('*.png'))
    texture_list=texture_jpg+texture_png
    l=sky_rng.choice(texture_list)
    blank_texture1=Texture(l)
    sky=Sky(texture=blank_texture1)
    return sky


def create_planets(positions,seed):
    visual_planet=[]
    path=Path('textures/planets')
    texture_jpg=list(path.glob('*.jpg'))
    texture_png=list(path.glob('*.png'))
    texture_list=texture_jpg+texture_png
    planet_rng=random.Random(seed) 
    for i in positions:
            
        l=planet_rng.choice(texture_list)
        blank_texture=Texture(l)
        visual_planet.append(Entity(model='sphere',color=color.white,scale=(system.planets[positions.index(i)].mass**0.27,system.planets[positions.index(i)].mass**0.27,system.planets[positions.index(i)].mass**0.27),position=(i[0]*10,0,i[1]*10),texture=blank_texture))
        texture_list.remove(l)   
    return visual_planet

def create_orbits(system):
    orbit=[]
    for i in range(len(system.planets)):
        orbit.append(Entity(model=Circle(mode='line',resolution=100,radius=system.planets[i].orbital_distance*10),color=color.white,position=(0,0,0),rotation=(90,0,0)))
    return orbit



def input(key):
    global seed
    global system
    global orbits
    global visual_planet
    global simulation_paused
    global simulation_speed
    global simulation_elapsed
    global text
    global sky
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
        simulation_speed=10
        simulation_elapsed=0
        seed=random.randint(0,10000000)
        for i in visual_planet:
            destroy(i)
        for i in orbits:
            destroy(i)
        destroy(star)
        destroy(sky)

        
        system=generate_system(seed)
        star=create_main_star(system)
        orbits=create_orbits(system)
        positions=current_position(system,simulation_elapsed)
        visual_planet=create_planets(positions,seed)
        sky=create_sky(seed)
        destroy(text)
        text=Text(text='PLANETARY SYSTEM\nSEED:{}\nSTAR MASS:{}\nPLANET COUNT:{}'.format(seed,system.star.mass,len(system.planets)),position=window.top_left)




EditorCamera(rotation_speed=200,zoom_speed=1.25)

app.run()              
