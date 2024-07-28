from controller import Robot, Camera, Motor, Receiver
import numpy as np

class HROSbot: 
    
    def __init__(self, bot):
        self.robot = bot
        self.robotTimestep = int(self.robot.getBasicTimeStep())
        self.TIMESTEP = 64
        self.speed = 10
        #
        self.ruedaDerechaSuperior = self.robot.getDevice("fr_wheel_joint")
        self.ruedaDerechaInferior = self.robot.getDevice("rr_wheel_joint")
        self.ruedaIzquierdaSuperior = self.robot.getDevice("fl_wheel_joint")
        self.ruedaIzquierdaInferior = self.robot.getDevice("rl_wheel_joint")
        #
        self.ruedaDerechaSuperior.setPosition(float('inf'))
        self.ruedaDerechaInferior.setPosition(float('inf'))
        self.ruedaIzquierdaInferior.setPosition(float('inf'))
        self.ruedaIzquierdaSuperior.setPosition(float('inf'))
        #
        self.giroscopio = self.robot.getDevice("imu gyro")
        self.acelerometro = self.robot.getDevice("imu accelerometer")
        self.lidar = self.robot.getDevice("laser")
        self.receiver = self.robot.getDevice("Receiver")
        #
        self.giroscopio.enable(self.robotTimestep)
        self.acelerometro.enable(self.robotTimestep)
        self.lidar.enable(self.robotTimestep)
        self.receiver.enable(self.robotTimestep)
        #
        self.frontLeftSensor = self.robot.getDevice("fl_range")
        self.frontRightSensor = self.robot.getDevice("fr_range")
        self.rearLeftSensor = self.robot.getDevice("rl_range")
        self.rearRightSensor = self.robot.getDevice("rr_range")
        #
        self.frontLeftSensor.enable(self.robotTimestep)
        self.frontRightSensor.enable(self.robotTimestep)
        self.rearLeftSensor.enable(self.robotTimestep)
        self.rearRightSensor.enable(self.robotTimestep)
        #
        self.frontLeftPositionSensor = self.robot.getDevice("front left wheel motor sensor")
        self.frontRightPositionSensor = self.robot.getDevice("front right wheel motor sensor")
        self.rearLeftPositionSensor = self.robot.getDevice("rear left wheel motor sensor")
        self.rearRightPositionSensor = self.robot.getDevice("rear right wheel motor sensor")
        #
        self.frontLeftPositionSensor.enable(self.TIMESTEP)
        self.frontRightPositionSensor.enable(self.TIMESTEP)
        self.rearLeftPositionSensor.enable(self.TIMESTEP)
        self.rearRightPositionSensor.enable(self.TIMESTEP)
        #
        self.anteriorValorPositionSensor = [0,0,0,0]
        self.DefaultPositionSensorAnterior()
        self.limiteSensor = 2.0
        # Detección de obstáculos
        self.minDistancia = 0.3
        self.toleranciaEntreSensores = 0.05
        self.epsilon = 0.01
        self.error_range = 3
        self.front_range = 25
        self.goal_index = 100
        self.minSignal = 0.5
        #
        self.radioRueda = 0.0425
        self.encoderUnit = (2*np.pi*self.radioRueda)/6.28 
        #
        self.receiver = self.robot.getDevice('Receiver')
        #
        self.receiver.enable(32)
 
    #

    def DisplayData(self,step):
        print("STEP #",step)
        print("   Acelerómetro:  ", self.acelerometro.getValues())
        print("   Giroscopio:    ", self.giroscopio.getValues())
        print("   Hay Obstáculo: ",self.getObstaculoAlFrente())
        print("   Hay Señal:     ", self.haySeñal())
        print("                   INT: ",self.receiver.getSignalStrength())

    # 

    def arrivedDestination(self):
        minSignalStrength = self.minSignal
        actualSignalStrength = self.receiver.getSignalStrength()
        print(actualSignalStrength)
        return actualSignalStrength >= minSignalStrength

    def haySeñal(self):
        return self.receiver.getQueueLength() > 0
    
##### Detección de obstáculos

    # Evita la repetición de código
    def getObstaculo(self,lidar_slice,extra=0):
        min = self.minDistancia + extra
        min_index = None
        for index in range(len(lidar_slice)):
            if lidar_slice[index] <= min:
                min = lidar_slice[index]
                min_index = index
        return min_index

    def getObstaculoAlFrente(self,extra=0):
        lidar_data = self.lidar.getRangeImage()
        fr = self.front_range # 50
        lidar_front = lidar_data[:fr] + lidar_data[-fr:]        # mitad primera: r, mitad izq: l
        obstaculo = self.getObstaculo(lidar_front, extra)                   # Retorna None o el número de index
        if obstaculo != None:
            if obstaculo < fr:
                lado = "right"
            else:
                lado = "left"
            return [obstaculo % self.front_range,lado]
        return None

    def getObstaculoADerecha(self,lidar_data):
        er = self.error_range
        lidar_right = lidar_data[self.right_goal_index - er : self.right_goal_index + er]
        return self.getObstaculo(lidar_right,0.2)

    def getObstaculoAIzquierda(self,lidar_data):
        er = self.error_range
        lidar_left = lidar_data[self.left_goal_index - er : self.left_goal_index + er]
        return self.getObstaculo(lidar_left,0.2)
    
####

    def DefaultPositionSensorAnterior(self):
        for i in range(3) :
            self.anteriorValorPositionSensor[i]=0

    def metrosRecorridos(self):
        ps_values = [0, 0]
        distancia = [0, 0]
        distancia[0]=0
        distancia[1]=0
        ps_values[0] = self.frontLeftPositionSensor.getValue()-self.anteriorValorPositionSensor[0]
        ps_values[1] = self.frontRightPositionSensor.getValue()-self.anteriorValorPositionSensor[1]
        #print("position values: {} {}".format(ps_values[0],ps_values[1]))
        for i in range(2):
            distancia[i] = ps_values[i]*self.encoderUnit

        #print("metros recorridos: {} {}".format(distancia[0], distancia[1]))
        return distancia;

<<<<<<< Updated upstream

    def avanzar(self, distancia, velocidad, metrosColision):
        #print("Avanzar")
=======
    def avanzar(self, distancia):
        print("Avanzar")
>>>>>>> Stashed changes
        dist = [0, 0]
        dist[0] = 0
        dist[1] = 0
        velocidad = self.speed
        self.robot.step(self.robotTimestep)
        fls =self.frontLeftSensor.getValue() 
        frs = self.frontRightSensor.getValue()
<<<<<<< Updated upstream

        velocidad_actual = 0
        aceleracion = 2  # Ajusta este valor según sea necesario para una aceleración más suave
        max_velocidad = self.speed

        while ((fls>metrosColision and frs>metrosColision)and
=======
        # while cierta condicion se cumpla
        while ((not self.getObstaculoAlFrente())and
>>>>>>> Stashed changes
               (dist[0]<distancia or dist[1]<distancia)and
               (self.robot.step(self.robotTimestep) != -1)):
            dist =  self.metrosRecorridos()

            if velocidad_actual < max_velocidad:
                velocidad_actual = min(velocidad_actual + aceleracion, max_velocidad)
            else:
                velocidad_actual = velocidad

            self.ruedaDerechaSuperior.setVelocity(velocidad_actual)
            self.ruedaDerechaInferior.setVelocity(velocidad_actual)
            self.ruedaIzquierdaInferior.setVelocity(velocidad_actual)
            self.ruedaIzquierdaSuperior.setVelocity(velocidad_actual)
            fls =self.frontLeftSensor.getValue() 
            frs = self.frontRightSensor.getValue()
            
        self.ruedaDerechaSuperior.setVelocity(0)
        self.ruedaDerechaInferior.setVelocity(0)
        self.ruedaIzquierdaInferior.setVelocity(0)
        self.ruedaIzquierdaSuperior.setVelocity(0)
        self.anteriorValorPositionSensor[0] = self.frontLeftPositionSensor.getValue()
        self.anteriorValorPositionSensor[1] = self.frontRightPositionSensor.getValue()
        
        if((dist[0]>=distancia) or (dist[1]>=distancia)):
            return True
        else:
            return False

    def retroceder(self, distancia, velocidad):
        #print("Retroceder")
        dist = [0, 0]
        distancia = -1*distancia
        self.robot.step(self.robotTimestep)
        rls = self.rearLeftSensor.getValue()
        rrs = self.rearRightSensor.getValue()

        dist[0] = 0
        dist[1] = 0

        if((rls>distancia and rrs>distancia)):
            while ((dist[0]>distancia or dist[1]>distancia)and(self.robot.step(self.robotTimestep) != -1)):
                dist =  self.metrosRecorridos()
                self.ruedaDerechaSuperior.setVelocity(-velocidad)
                self.ruedaDerechaInferior.setVelocity(-velocidad)
                self.ruedaIzquierdaInferior.setVelocity(-velocidad)
                self.ruedaIzquierdaSuperior.setVelocity(-velocidad)
            
        self.ruedaDerechaSuperior.setVelocity(0)
        self.ruedaDerechaInferior.setVelocity(0)
        self.ruedaIzquierdaInferior.setVelocity(0)
        self.ruedaIzquierdaSuperior.setVelocity(0)
        self.anteriorValorPositionSensor[0] = self.frontLeftPositionSensor.getValue()
        self.anteriorValorPositionSensor[1] = self.frontRightPositionSensor.getValue()
    

    def giroDerecha(self, angulo):
        print("Derecha")
        velocidad = 2.0
        ang_z = 0
<<<<<<< Updated upstream
=======
        giro = True
>>>>>>> Stashed changes

        self.robot.step(self.robotTimestep)
        """
        fls =self.frontLeftSensor.getValue() 
        frs = self.frontRightSensor.getValue()

        if(((fls<=frs+self.toleranciaEntreSensores))or
           ((fls==self.limiteSensor)and(frs==self.limiteSensor))):
            
<<<<<<< Updated upstream
            while ((self.robot.step(self.robotTimestep) != -1) and (not self.hayObstaculo()) and (ang_z>(angulo))):
                gyroZ =self.giroscopio.getValues()[2]
                ang_z=ang_z+(gyroZ*self.robotTimestep*0.001)
            
                self.ruedaDerechaSuperior.setVelocity(0.0)
                self.ruedaDerechaInferior.setVelocity(0.0)
                self.ruedaIzquierdaInferior.setVelocity(velocidad)
                self.ruedaIzquierdaSuperior.setVelocity(velocidad)
=======
            giro = True
        """
        while ((self.robot.step(self.robotTimestep) != -1)and(ang_z>(angulo))):
            gyroZ =self.giroscopio.getValues()[2]
            ang_z=ang_z+(gyroZ*self.robotTimestep*0.001)
        
            self.ruedaDerechaSuperior.setVelocity(0.0)
            self.ruedaDerechaInferior.setVelocity(0.0)
            self.ruedaIzquierdaInferior.setVelocity(velocidad)
            self.ruedaIzquierdaSuperior.setVelocity(velocidad)
>>>>>>> Stashed changes
            
        self.ruedaDerechaSuperior.setVelocity(0)
        self.ruedaDerechaInferior.setVelocity(0)
        self.ruedaIzquierdaInferior.setVelocity(0)
        self.ruedaIzquierdaSuperior.setVelocity(0)


    def giroIzquierda(self, angulo):
        print("izquierda")
        velocidad = 2.0
        ang_z = 0
<<<<<<< Updated upstream
=======
        giro = True
>>>>>>> Stashed changes

        self.robot.step(self.robotTimestep)
        """
        fls =self.frontLeftSensor.getValue() 
        frs = self.frontRightSensor.getValue()

        if(((frs<=fls+self.toleranciaEntreSensores))or
           ((fls==self.limiteSensor)and(frs==self.limiteSensor))):
<<<<<<< Updated upstream

            while ((self.robot.step(self.robotTimestep) != -1) and (not self.hayObstaculo()) and(ang_z<(angulo))): #0.5*np.pi
                gyroZ =self.giroscopio.getValues()[2]
                ang_z=ang_z+(gyroZ*self.robotTimestep*0.001)
            
                self.ruedaDerechaSuperior.setVelocity(velocidad)
                self.ruedaDerechaInferior.setVelocity(velocidad)
                self.ruedaIzquierdaInferior.setVelocity(0.0)
                self.ruedaIzquierdaSuperior.setVelocity(0.0)
=======
            
            giro = True
        """
        while ((self.robot.step(self.robotTimestep) != -1)and(ang_z<(angulo))): #0.5*np.pi
            gyroZ =self.giroscopio.getValues()[2]
            ang_z=ang_z+(gyroZ*self.robotTimestep*0.001)
        
            self.ruedaDerechaSuperior.setVelocity(velocidad)
            self.ruedaDerechaInferior.setVelocity(velocidad)
            self.ruedaIzquierdaInferior.setVelocity(0.0)
            self.ruedaIzquierdaSuperior.setVelocity(0.0)
>>>>>>> Stashed changes
            
        self.ruedaDerechaSuperior.setVelocity(0)
        self.ruedaDerechaInferior.setVelocity(0)
        self.ruedaIzquierdaInferior.setVelocity(0)
        self.ruedaIzquierdaSuperior.setVelocity(0)

    def vaciarCola(self):
        while(self.receiver.getQueueLength() > 0):
            self.receiver.nextPacket()