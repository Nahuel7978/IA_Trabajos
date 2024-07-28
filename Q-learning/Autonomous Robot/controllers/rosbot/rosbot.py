"""my_controller_rosbot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Receiver
from Movimientos.HROSbot import * 
from Movimientos.HROSbotComportamental import * 
import numpy as np
import math
import time
import struct

# create the Robot instance.
robot = Robot()
# get the time step of the current world. 
timestep = int(robot.getBasicTimeStep()) # timestep = 32 


receiver = robot.getDevice('Receiver')
receiver.enable(timestep)
#print(receiver.getQueueLength())

rosbot = HROSbotComportamental(robot)
#rosbot.avanzar(0.01,5,rosbot.minDistancia)

llegue = False

step_counter = 0
while(robot.step(timestep)!=-1) and (not llegue):
    print(receiver.getSignalStrength())
    rosbot.DisplayData(step_counter)
    step_counter+=1
    obstaculo = rosbot.getObstaculoAlFrente()
    print("Intensidad de la señal",rosbot.receiver.getSignalStrength())
    if (rosbot.arrivedDestination()):
        print("   FIN DEL RECORRIDO: Objetivo alcanzado.")
        llegue = True
    elif (obstaculo != None):
        print("   DECISIÓN: Esquivar obstáculo")
        rosbot.evitarObstaculo(obstaculo)
    elif (rosbot.haySeñal()):
        print("   DECISIÓN: Ir Hacia Estimulo")
        llegue = rosbot.ir_estimulo()
    else:
        print("   DECISIÓN: Explorar")
        rosbot.explorar()

print(llegue)
print("END")

"""
rosbot.avanzar(1,5.0)
rosbot.avanzar(1,5.0)
rosbot.avanzar(1,5.0)
rosbot.avanzar(1,5.0)
rosbot.avanzar(1,5.0)
rosbot.giroIzquierda()
rosbot.avanzar(1,5.0)

"""

#c = 299792458  
"""
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    print("Queue: ",receiver.getQueueLength())
    if receiver.getQueueLength() > 0:
        message = receiver.getFloats()
        
        tiempo_emision = message[0]
           
        tiempo_recepcion = time.time()
        
        dif=tiempo_recepcion-tiempo_emision
        
        distancia = (c * dif)/2
        
        direccion = receiver.getEmitterDirection()
        
        fuerza = receiver.getSignalStrength() # 1/r^2
        
        distancia = math.sqrt(1/fuerza)
        
        print(f"Received signal: {tiempo_emision}")
        print("Tiempo de de recepcion: ", tiempo_recepcion)
        print("Tiempo que tardo: ", dif)
        print("Distancia: ", distancia)
        print("Fuerza: ",fuerza)
        print(f"Direccion: x =  {direccion[0]} ; y= {direccion[1]} ; z = {direccion[2]} ")
        print("angulo: ",math.atan2(direccion[1], direccion[0]))

        while(receiver.getQueueLength() > 0):
            receiver.nextPacket()
    else:
        print("NAti")
    
    fin = rosbot.avanzar(1,5.0,0.3)
    if(not fin):
        print("El recorrido NO termino")
    else:
        print("El recorrido Termino")
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
  #  pass

# Enter here exit cleanup code.
"""