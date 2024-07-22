
from controller import Robot, Motor, Receiver
from Movimientos.HROSbot import *
import math

class HROSbotComportamental(HROSbot):

    def __init__(self, bot):
        super().__init__(bot)
<<<<<<< Updated upstream
=======
        self.exploracion = False
        self.anguloAnterior = 0.5
        self.maximoGiroDerecha = 0.5
        self.maximoGiroIzquierda = 0.5
>>>>>>> Stashed changes

    def ir_estimulo(self):
        self.robot.step(self.robotTimestep)
        print("--> Ir_estimulo: ", self.receiver.getQueueLength() )
        estimuloEncontrado = False
        velocidad = 5.0
        tolerancia = 0.1
        finaliza = False

        if(self.receiver.getQueueLength() > 0):
            direccion = self.receiver.getEmitterDirection() #1: x; 2: y; 3:z;

            if(direccion[0]<1):
                if(direccion[1]>0):
                    self.giroIzquierda(math.atan2(direccion[1], direccion[0]))
                else:
                    self.giroDerecha(math.atan2(direccion[1], direccion[0]))

<<<<<<< Updated upstream
            distancia = math.sqrt(1/self.receiver.getSignalStrength())
=======
                self.actualizarOrientación(angulo)
                
            distancia = self.distanciaSeñal()
>>>>>>> Stashed changes

            finaliza = self.avanzar(distancia,velocidad)
            self.vaciarCola()
            
            self.robot.step(self.robotTimestep)

        return finaliza


    def evitarObstaculo(self):
        print("--> EvitarObstaculo")
        return None 

    def explorar(self):
<<<<<<< Updated upstream


        return None
            
        
                
=======
        print("-->Explorar")
        self.robot.step(self.robotTimestep)
        velocidad = 5
        distancia = 2

        if(self.receiver.getQueueLength() <= 0):
            self.exploracion=True
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

    
>>>>>>> Stashed changes
