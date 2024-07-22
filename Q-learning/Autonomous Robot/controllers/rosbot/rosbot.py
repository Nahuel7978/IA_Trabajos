"""my_controller_rosbot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Receiver, Supervisor
from Movimientos.HROSbot import * 
from Movimientos.HROSbotComportamental import * 
from Movimientos.HROSbotInteligente import * 
from Movimientos.EntornoEntrenamiento import * 
from Movimientos.SupervisorClass import * 
import numpy as np
import math
import time
import struct


# create the Robot instance.

robot = Robot()
timestep =  int(robot.getBasicTimeStep())

<<<<<<< Updated upstream
rosbot = HROSbotComportamental(robot)

rosbot.avanzar(0.01,0.1,0.3)
if(rosbot.ir_estimulo()):
    print("Funco")
=======
rosbot = HROSbotInteligente(robot,0.1,0.7,0.1)
#pInicial, recompensaMaxima, recompensaMinima, valorPaso, penalizacion, epocas, pasos
entorno = EntornoEntrenamiento(10,5,-1,-5,10,20)

llegue = False


entorno.entrenamiento(rosbot)
#uActual = entorno.ubicacionActual()
#rActual = entorno.rotacionActual()

"""
while(robot.step(timestep) != -1)and(not llegue):
    if(rosbot.get_receiver() > 0):
        print("Ir Estimulo")
        rosbot.ir_estimulo()
        llegue =  rosbot.estimuloEncontrado(0.1)
    else:
        print("Explorar")
        rosbot.explorar()
        
#☺    entorno.puntoInicial(uActual,rActual)

>>>>>>> Stashed changes
"""
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