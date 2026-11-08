from ursina import *   
from asterion import *
seed=50
system=generate_system(seed)
simulation_speed=10
simulation_elapsed=0
positions=current_position(system,simulation_elapsed)
app=Ursina()
visual_star=Entity(model='sphere',color=color.yellow,scale=(3,3,3),position=(0,0,0))
visual_planet=[]
for i in positions:
    visual_planet.append(Entity(model='sphere',color=color.blue,scale=(1,1,1),position=(i[0]*10,0,i[1]*10)))




simulation_paused=False
def update():
    global simulation_elapsed
    if simulation_paused==False:
        simulation_elapsed+=time.dt*simulation_speed
        position=current_position(system,simulation_elapsed)
        for i in range(len(position)):
            visual_planet[i].position=(position[i][0]*10,0,position[i][1]*10)

def input(key):
    global simulation_paused
    global simulation_speed
    if key=='space':
        simulation_paused=not simulation_paused
    if key=='up arrow':
        simulation_speed+=1
    if key=='down arrow':
        if simulation_speed-1>0:
            simulation_speed-=1
        else:
            simulation_speed=1



app.run()              
