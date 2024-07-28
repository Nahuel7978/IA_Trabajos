
from controller import Robot, Motor, Receiver
from Movimientos.HROSbot import *
import math
import numpy as np

class HROSbotComportamental(HROSbot):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot
        self.exploracion = False
        self.anguloAnterior = 0.5
        self.maximoGiroDerecha = 0.25
        self.maximoGiroIzquierda = 0.25

    def ir_estimulo(self):
        self.robot.step(self.robotTimestep)
        #print("Ir_estimulo. #Señales ", self.receiver.getQueueLength() )
<<<<<<< Updated upstream
        estimuloEncontrado = False
        velocidad = self.speed
        metrosColision = self.minDistancia
        tolerancia = 0.1
=======
        finaliza = False
>>>>>>> Stashed changes

        if (self.getObstaculoAlFrente()==None and self.haySeñal()):
            direccion = self.receiver.getEmitterDirection() #1: x; 2: y; 3:z;
            
            if (direccion[0]<1):
                angulo = math.atan2(direccion[1], direccion[0])
                if(direccion[1]>0):
                    self.giroIzquierda(angulo)
                else:
                    self.giroDerecha(angulo)
                self.actualizarOrientación(angulo)
            distancia = math.sqrt(1/self.receiver.getSignalStrength())
            #print("   - HAY SEÑAL. Dirección ",print(direccion),"; Distancia: ",distancia)

<<<<<<< Updated upstream
            #print("Distancia: ",distancia)
            finaliza = self.avanzar(distancia,velocidad,metrosColision)
            self.vaciarCola()
            self.robot.step(self.robotTimestep)

            if (finaliza):
                estimuloEncontrado = True
            else:
                if(self.receiver.getQueueLength() > 0):
                    #print("Queue: ", self.receiver.getQueueLength())
                    distancia = math.sqrt(1/self.receiver.getSignalStrength())
                    #print("Segunda distancia: ",distancia)
                    if(distancia<=(metrosColision+tolerancia)):
                        estimuloEncontrado = True

        return estimuloEncontrado
=======
                self.actualizarOrientación(math.atan2(direccion[1], direccion[0]))

            distancia = self.distanciaSeñal()
            self.avanzar(distancia)
            intensidad = self.receiver.getSignalStrength()
            print("INTENSIDAD: ",intensidad)
            finaliza = intensidad > 0.4
            self.vaciarCola()
            self.robot.step(self.robotTimestep)

        return finaliza
    
    def getClosestDistance(self,lidar_data):
        closestDistance = float("inf")
        index_closestDistance = -1
        for index in range(len(lidar_data)):
            if lidar_data[index] < closestDistance:
                closestDistance = lidar_data[index]
                index_closestDistance = index
        print("Elemento: ",index_closestDistance, "; Menor distancia: ",closestDistance)
        return [index_closestDistance, closestDistance]

    def getPuntoEnGrados(self,index,cant_puntos=400.0):
        grados_por_punto = 360.0 / float(cant_puntos)
        angulo = float(index) * grados_por_punto
        return angulo
    
    def getPuntoEnRadianes(self,index,cant_puntos=400.0):
        radianes_por_punto = 2 / float(cant_puntos)
        angulo = float(index) * radianes_por_punto
        return angulo
>>>>>>> Stashed changes

    def getAnguloDeGiro(self,cd_index,goal_index):
        cd_index_en_radianes = self.getPuntoEnRadianes(cd_index)
        goal_index_en_radianes = self.getPuntoEnRadianes(goal_index)
        radianes = abs( cd_index_en_radianes - goal_index_en_radianes )
        print("Gran Giro: ",radianes)
        return radianes - 0.1

    def getAnguloDeCorreccion(self,side_slice):
        umbral_error = 0.05

        n = len(side_slice)
        if n % 2 == 0 or n < 3:
            raise ValueError("La lista de distancias debe tener un número impar de elementos y al menos 3 elementos.")

        medio = n // 2

        for i in range(1, medio + 1):
            error_actual = side_slice[medio + i] - side_slice[medio - i]
            if abs(error_actual) > umbral_error:
                angulo_correccion = np.sign(error_actual) * (i * (2 * np.pi / 400))  # Convertir a radianes y dar dirección
                print(angulo_correccion)
                return angulo_correccion

        return 0  # Si no hay corrección necesaria

    def evitarObstaculo(self, obstaculo):

        error_range = self.error_range
        front_range = self.front_range
        goal_index = self.goal_index
        
        lidar_data = self.lidar.getRangeImage()
        min = 0
        max = len(lidar_data)-1
        
        lidar_front_right = lidar_data[min:min+front_range]
        lidar_front_left = lidar_data[-(max+1):-(max-front_range+1)]
        print(len(lidar_front_left)-len(lidar_front_right))

        # Obstáculo en frente-derecha
        # si el obstáculo está en frente derecha doblo a la izquierda
        if (obstaculo[1] == "right"):
            print("  OBSTACULO DER: ", obstaculo[0])
            
            # Gran giro a izquierda.
            angulo = self.getAnguloDeGiro(obstaculo[0],goal_index)
            self.giroIzquierda(angulo*np.pi)
            """
            # Correción de giro.
            while True:
                lidar_data = self.lidar.getRangeImage()[goal_index-error_range:goal_index+error_range+1]
                angulo_correccion = self.getAnguloDeCorreccion(lidar_data)
                if angulo_correccion == 0:
                    break
                print(f"Corrigiendo giro a la izquierda: {angulo_correccion} radianes.")
                self.giroIzquierda(angulo_correccion*np.pi)
            """
            # Avance
            print(self.getObstaculoADerecha(self.lidar.getRangeImage()))
            while (self.getObstaculoAlFrente()!=None): #and self.getObstaculoADerecha(lidar_data)
                self.avanzar(1)
                lidar_data = self.lidar.getRangeImage()

        # Obstáculo en frente-izquierda
        #elif (self.hayObstaculo(lidar_front_left)) or self.hayObstaculoAIzquierda(lidar_data):
        if (obstaculo[1] == "left"):

            index_cd = self.getClosestDistance(lidar_front_left)[0]
            print("  OBSTACULO IZQ: ", index_cd)
            # Gran giro a derecha.
            angulo = self.getAnguloDeGiro(obstaculo[0],goal_index)
            self.giroDerecha(-angulo*np.pi)
            """
            # Correción de giro.
            angulo = 0.01
            #cd = self.getClosestDistance(self.lidar.getRangeImage())
            lidar_data = self.lidar.getRangeImage()
            while (lidar_data[left_goal_index - self.error_range] > lidar_data[left_goal_index + self.error_range]):
                self.giroDerecha(-angulo*np.pi)
                lidar_data = self.lidar.getRangeImage()
                cd = self.getClosestDistance(self.lidar.getRangeImage())
            while True:
                lidar_data = self.lidar.getRangeImage()[-(goal_index+error_range+1):-(goal_index-error_range)]
                angulo_correccion = self.getAnguloDeCorreccion(lidar_data)
                if angulo_correccion == 0:
                    break
                print(f"Corrigiendo giro a la derecha: {angulo_correccion} radianes.")
                self.giroDerecha(-angulo_correccion*np.pi)
            """
            # Avance
            print(self.getObstaculoAlFrente())
            while (self.getObstaculoAlFrente(-0.5)!=None): #and self.getObstaculoAIzquierda(self.lidar.getRangeImage())
                self.avanzar(1)
 

        #lidar_data = self.lidar.getRangeImage()
        #print(lidar_data[:30] + lidar_data[-30:] )
        return None 

    """
    def evitarObstaculo(self):
        #print("Evitar Obstáculo")
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

        
        return None 
    """

    def explorar(self):
        self.robot.step(self.robotTimestep)
        velocidad = self.speed
        distancia = 2
        metrosColision = self.minDistancia

        if not self.haySeñal():
            self.exploracion = True
            giro = np.random.uniform()
            if (giro <= 0.5):
                angulo = np.random.uniform(low=0, high=self.maximoGiroIzquierda)
                self.giroIzquierda(angulo*np.pi)
                self.actualizarOrientación(angulo)
            else:
                angulo = -1*np.random.uniform(low=0, high=self.maximoGiroDerecha)
                self.giroDerecha(angulo*np.pi)
                self.actualizarOrientación(angulo)

<<<<<<< Updated upstream
            self.avanzar(distancia,velocidad,metrosColision)    
=======
            self.avanzar(distancia)    
>>>>>>> Stashed changes
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

        #print("Angulo Ant: ", self.anguloAnterior)
        #print("Maximo Izq: ", self.maximoGiroIzquierda)
        #print("Maximo Der: ", self.maximoGiroDerecha)
        #print("Angulo Giro: ", angulo)
        
                