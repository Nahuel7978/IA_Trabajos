
from controller import Robot, Motor, Receiver
from Movimientos.HROSbot import *
import math

class HROSbotComportamental(HROSbot):

    def __init__(self, bot):
        super().__init__(bot)

    def ir_estimulo(self):
        self.robot.step(self.robotTimestep)
        print("Ir_estimulo: ", self.receiver.getQueueLength() )
        estimuloEncontrado = False
        velocidad = 5.0
        metrosColision = 0.3
        tolerancia = 0.1

        if(self.receiver.getQueueLength() > 0):
            print("HAY SEÑAL")
            direccion = self.receiver.getEmitterDirection() #1: x; 2: y; 3:z;

            if(direccion[0]<1):
                if(direccion[1]>0):
                    self.giroIzquierda(math.atan2(direccion[1], direccion[0]))
                else:
                    self.giroDerecha(math.atan2(direccion[1], direccion[0]))

            distancia = math.sqrt(1/self.receiver.getSignalStrength())

            print("Distancia: ",distancia)
            finaliza = self.avanzar(distancia,velocidad,metrosColision)
            self.vaciarCola()
            
            self.robot.step(self.robotTimestep)

            if(finaliza):
                estimuloEncontrado = True
            else:
                if(self.receiver.getQueueLength() > 0):
                    print("Queue: ", self.receiver.getQueueLength())
                    distancia = math.sqrt(1/self.receiver.getSignalStrength())
                    print("Segunda distancia: ",distancia)
                    if(distancia<=(metrosColision+tolerancia)):
                        estimuloEncontrado = True

        return estimuloEncontrado

    def evitarObstaculo(self):
        
        return None 

    def explorar(self):


        return None
            
        
                