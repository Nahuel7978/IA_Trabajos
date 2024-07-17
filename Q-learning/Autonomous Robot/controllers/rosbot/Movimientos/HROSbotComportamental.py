
from controller import Robot, Motor, Receiver
from Movimientos.HROSbot import *
import math
import numpy as np

class HROSbotComportamental(HROSbot):

    def __init__(self, bot):
        super().__init__(bot)
        self.exploracion = False
        self.anguloAnterior = 0.5
        self.maximoGiroDerecha = 0.5
        self.maximoGiroIzquierda = 0.5


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
                angulo=math.atan2(direccion[1], direccion[0])
                if(direccion[1]>0):
                    self.giroIzquierda(angulo)
                else:
                    self.giroDerecha(angulo)

                self.actualizarOrientación(angulo)
                
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
        self.robot.step(self.robotTimestep)
        velocidad = 5
        distancia = 2
        metrosColision = 0.3

        if(self.receiver.getQueueLength() <= 0):
            self.exploracion=True
            giro = np.random.uniform()
            if(giro<=0.5):
                angulo = np.random.uniform(low=0, high=self.maximoGiroIzquierda)
                self.giroIzquierda(angulo*np.pi)

                self.actualizarOrientación(angulo)
            else:
                angulo = -1*np.random.uniform(low=0, high=self.maximoGiroDerecha)
                self.giroDerecha(angulo*np.pi)

                self.actualizarOrientación(angulo)

            self.avanzar(distancia,velocidad,metrosColision)    
            self.exploracion=False

    def actualizarOrientación(self, angulo):
        if(self.exploracion):
            anguloActual=angulo+self.anguloAnterior
            self.maximoGiroIzquierda=self.maximoGiroIzquierda-angulo
            self.maximoGiroDerecha= anguloActual
            self.anguloAnterior=anguloActual
        else:
            self.anguloAnterior = 0.5
            self.maximoGiroDerecha = 0.5
            self.maximoGiroIzquierda = 0.5

        print("Angulo Ant: ", self.anguloAnterior)
        print("Maximo Izq: ", self.maximoGiroIzquierda)
        print("Maximo Der: ", self.maximoGiroDerecha)
        print("Angulo Giro: ", angulo)
        
                