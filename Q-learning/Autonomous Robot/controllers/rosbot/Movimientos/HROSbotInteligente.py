
from Movimientos.HROSbotComportamental import * 
import numpy as np

class HROSbotInteligente(HROSbotComportamental):
    def __init__(self, bot, l_rate, t_descuento, r_exploracion):
        super().__init__(bot)

        self.learning_rate =l_rate
        self.tasa_descuento = t_descuento #si esta cerca de 1 busca las recompensas lejanas
        self.prob_exploracion = r_exploracion

        self.cantidadAcciones = 3 #tres comportamientos
        self.cantidadEstados = 6 #seis estados posibles

        #Inicializo la tabla de politicas con valores cercanos a ceros para agilizar la exploración, pero
        #minimizando el sesgo.
        self.qLearning = np.random.uniform(0, 0.05, size=(self.cantidadAcciones, self.cantidadEstados))
        

    #-Devuelve la posicion del estado actual en la tabla de politicas.
    def estadoActual(self):
        indice = 0
        self.robot.step(self.robotTimestep)
        frs = self.frontRightSensor.getValue() 
        fls = self.frontLeftSensor.getValue() 
        Queque = self.receiver.getQueueLength()

        if((frs>=self.limiteSensor)and(fls>=self.limiteSensor)): #No detecta obtaculos
            if((Queque<=0)): #No Hay señal
                indice = 0
            else:   #Hay señal
                indice = 1
        elif((frs<=self.minDistancia)and(fls<=self.minDistancia)): #Hay obstaculo
            if((Queque<=0)): #No hay señal
                indice = 2
            else:   #Hay señal
                indice = 3
        elif((frs>self.minDistancia)and(fls>self.minDistancia)): #Obstaculo lejos
            if((Queque<=0)): #No hay señal
                indice = 4
            else:   #Hay señal
                indice = 5

        return indice
    
    #--Determina la siguiente accion a tomar.
    def siguienteAccion(self, estadoActual):
        explorar = np.random.uniform()
        sigAccion = 0

        #Determino si la siguiente acción es explorar.
        if(explorar<=self.prob_exploracion):
            sigAccion = np.random.randint(self.cantidadAcciones) 
        else:
            sigAccion = np.argmax(self.qLearning[:,estadoActual])

        return sigAccion

    #--Actualizacion por el método de Sarsa. 
    def actualizarPoliticas(self, estadoActual, accionTomada, estadoSiguiente, accionSiguiente, recompensa):
        #Q(s,a)
        qActual = self.qLearning[accionTomada][estadoActual]
        print("qActual: qLearning[",accionTomada,"][",estadoActual,"]= ",qActual)

        #Q(s',a')
        qSiguiente = self.qLearning[accionSiguiente][estadoSiguiente]

        print("qSiguiente: qLearning[",accionSiguiente,"][",estadoSiguiente,"]= ",qSiguiente)

        ## Q(s,a) = Q(s,a)+ lr*(r + td*Q(s',a')-Q(s,a))
        self.qLearning[accionTomada][estadoActual] = qActual + (self.learning_rate*(recompensa+(self.tasa_descuento*qSiguiente)-qActual))

        print("qActual Mej: qLearning[",accionTomada,"][",estadoActual,"]= ",self.qLearning[accionTomada][estadoActual])

    #--Ejecuta el comportamiento pertinente
    def ejecutarComportamiento(self, accion):
        if(accion==0):
            self.ir_estimulo()
        elif(accion==1):
            self.evitarObstaculo()
        elif(accion==2):
            self.explorar()

    #--Ejecuta los comportamientos en base a lo aprendido
    def vivir(self):
        estAct = self.estadoActual()
        sigAcc = self.siguienteAccion(estAct)
        self.ejecutarAccion(sigAcc)