"""my_controller_rosbot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Receiver, Supervisor
from Movimientos.HROSbot import * 
from Comportamientos.HROSbotComportamental import * 
from Inteligente.HROSbotInteligente import * 
from Inteligente.EntornoEntrenamiento import * 
import numpy as np
import math

# create the Robot instance.

robot = Robot()
# get the time step of the current world. 
timestep = int(robot.getBasicTimeStep()) # timestep = 32 

rosbot = HROSbotInteligente(robot,0.1,0.7,0.2)

entorno = EntornoEntrenamiento(5,2,1,-5,10,20)

rosbotComp = HROSbotComportamental(robot)
llegue = False

rosbot.visualizarPoliticas()

rosbot.cargarPoliticas()
rosbot.visualizarPoliticas()

#entorno.entrenamiento(rosbot)    
#entorno.visualizarRegistroEntrenamiento()
#rosbot.visualizarPoliticas()

print("--------------")
print("MODELO ENTRENADO")
print("--------------")
i=1
while((robot.step(timestep) != -1)and(not llegue)):
    print("--->Accion",i,"<---")
    i+=1
    rosbot.vivir()
    llegue =  rosbot.estimuloEncontrado(0.1)
    print("--------------")
    
rosbot.displayMapa()

"""#Braitenberg
while(robot.step(timestep) != -1)and(not llegue):
    print("------Nuevo Paso----------")
    if(rosbotComp.getObstaculoAlFrente() != None):
        print("Evitar Obstaculo")
        rosbotComp.evitarObstaculoGuiado()
    elif(rosbotComp.get_receiver() > 0):
        print("Ir Estimulo")
        rosbotComp.ir_estimulo()
        llegue =  rosbotComp.estimuloEncontrado(0.1)
    else:
        print("Explorar")
        rosbotComp.explorarDos()
"""