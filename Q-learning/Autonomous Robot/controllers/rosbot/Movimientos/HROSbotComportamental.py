
from controller import Robot, Motor, Receiver
from Movimientos.HROSbot import *
import math
import numpy as np

class HROSbotComportamental(HROSbot):

    def __init__(self, bot):
        super().__init__(bot)
        self.exploracion = False
        self.anguloAnterior = 0.5
        self.maximoGiroDerecha = 0.25
        self.maximoGiroIzquierda = 0.25

    def ir_estimulo(self):
        self.robot.step(self.robotTimestep)
        print("--> Ir_estimulo.  ", self.receiver.getQueueLength() )
        velocidad = self.speed
        finaliza = False

        if (self.haySeñal()):
            direccion = self.receiver.getEmitterDirection() #1: x; 2: y; 3:z;
            if (direccion[0]<1):
                if(direccion[1]>0):
                    self.giroIzquierda(math.atan2(direccion[1], direccion[0]))
                else:
                    self.giroDerecha(math.atan2(direccion[1], direccion[0]))

                self.actualizarOrientación(math.atan2(direccion[1], direccion[0]))
                
            distancia = self.distanciaSeñal()

            finaliza = self.avanzar(distancia,velocidad)
            self.vaciarCola()
            self.robot.step(self.robotTimestep)

        return finaliza



    def evitarObstaculo(self):
        print("--> Evitar Obstáculo")
        self.robot.step(self.robotTimestep)
        velocidad = self.speed
        min = self.minDistancia
        flsv = self.frontLeftSensor.getValue()  # Front Left Sensor Value
        frsv = self.frontRightSensor.getValue() # Front Right Sensor Value       
        while (self.hayObstaculo()): # Hay un obstáculo en el camino
            # Clara decisión de giro: ángulo de giro menor a un lado determinado
            if (flsv < 0.1 or frsv < 0.1):
                self.retroceder(0.05,velocidad)
            if (abs(flsv - frsv) > self.toleranciaEntreSensores):
                angulo = 0.1
                if (frsv > flsv):   # Giro a la derecha
                    self.giroDerecha(-angulo*np.pi)
                    self.retroceder(0.2,velocidad)
                    self.giroDerecha(-angulo*np.pi)
                else:
                    self.giroIzquierda(angulo*np.pi)
                    self.retroceder(0.2,velocidad)
                    self.giroIzquierda(angulo*np.pi)
            # Decisión de giro ambigüa: ángulo de giro mayor a un lado aleatorio
            else:
                #print("DECISION DE GIRO AMBIGUA")
                angulo = 0.25
                giro = np.random.uniform()
                if (giro <= 1/3):
                    self.giroIzquierda(angulo*np.pi)
                    self.retroceder(0.2,velocidad)
                    self.giroIzquierda(angulo*np.pi)
                elif (giro <= 2/3):
                    self.giroDerecha(-angulo*np.pi)
                    self.retroceder(0.2,velocidad)
                    self.giroDerecha(-angulo*np.pi)
            self.avanzar(0.2,self.speed) 
            flsv = self.frontLeftSensor.getValue()
            frsv = self.frontRightSensor.getValue()
        self.actualizarOrientación(0.0)
        self.vaciarCola()
        self.robot.step(self.robotTimestep)

    def explorar(self):
        print("--> Expplorar")
        self.robot.step(self.robotTimestep)
        velocidad = self.speed
        distancia = 2

        if (not self.haySeñal()):
            self.exploracion = True
            probMov = np.random.uniform()

            if((probMov<=0.30) or (self.hayObstaculo())):
                probGiro = np.random.uniform()
                giro = False
                i = 0
                while((not giro)and(i<=1)):
                    i +=1
                    if(probGiro<=0.5):
                        angulo = np.random.uniform(low=0, high=self.maximoGiroIzquierda)
                        giro = self.giroIzquierda(angulo*np.pi)
                        if(giro):
                            self.actualizarOrientación(angulo)
                        else:
                            probGiro = 0.9
                    else:
                        angulo = -1*np.random.uniform(low=0, high=self.maximoGiroDerecha)
                        giro = self.giroDerecha(angulo*np.pi)
                        
                        if(giro):
                            self.actualizarOrientación(angulo)
                        else:
                            probGiro = 0.1
                if(giro):
                    self.avanzar(distancia,velocidad)    
            else:
                self.avanzar(distancia,velocidad)

            self.exploracion=False
            self.vaciarCola()
            self.robot.step(self.robotTimestep)

    def actualizarOrientación(self, angulo):
        if(self.exploracion):
            anguloActual=angulo+self.anguloAnterior
            self.maximoGiroIzquierda=self.maximoGiroIzquierda-angulo
            self.maximoGiroDerecha= anguloActual
            self.anguloAnterior=anguloActual
        else:
            self.anguloAnterior = 0.5
            self.maximoGiroDerecha = 0.25
            self.maximoGiroIzquierda = 0.25

    
