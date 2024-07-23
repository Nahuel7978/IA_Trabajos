import numpy as np
from Movimientos.HROSbotInteligente import *
from controller import Supervisor

class EntornoEntrenamiento():

    def __init__(self, recompensaMaxima, recompensaMinima, valorPaso, penalizacion, epocas, pasos):

        self.recompensaMaxima = recompensaMaxima
        self.recompensaMinima = recompensaMinima
        self.penalizacionMaxima = penalizacion
        self.penalizacionMinima = valorPaso

        self.epocas = epocas
        self.pasos = pasos

        self.supervisor = Supervisor()
        self.robot_node = self.supervisor.getFromDef("principal_robot")
        self.timestep = int(self.supervisor.getBasicTimeStep())
        self.translation = self.robot_node.getField("translation")
        self.rotation = self.robot_node.getField("rotation")

        self.toleranciaMovimiento = 1


    def determinarRecompensa(self, robot,antValPos):
        
        actValPosDer = round(robot.get_frontRightPositionSensor(), 1)
        actValPosIzq = round(robot.get_frontLeftPositionSensor(), 1)
        senal = robot.get_receiver()
        recompensa =  0
        movimiento = False

        print(antValPos[0]+self.toleranciaMovimiento,">",actValPosIzq," and ",antValPos[1]+self.toleranciaMovimiento,">",actValPosDer )
        if((antValPos[0]+self.toleranciaMovimiento>actValPosIzq) and(antValPos[1]+self.toleranciaMovimiento>actValPosDer)):
             recompensa = self.penalizacionMaxima
        else:
            movimiento=True

        if(senal>0):
            tolerancia = 0.1 
            if(robot.estimuloEncontrado(tolerancia)):
                recompensa = self.recompensaMaxima
            elif(movimiento):
                recompensa = self.recompensaMinima
        
        elif(movimiento):
            recompensa = self.penalizacionMinima

        print("|--> Recompensa: ", recompensa)
        return recompensa

    def entrenamiento(self, robot):

        uInicial = self.ubicacionActual()
        rInicial = self.rotacionActual()
        
        for i in range(self.epocas):
            objAlcanzado=False
            j = 0
            estSig = robot.estadoActual()
            siguienteAccion = robot.siguienteAccion(estSig)
            antValPos= [0,0]
            actValPosDer = round(robot.get_frontRightPositionSensor(),1)
            actValPosIzq = round(robot.get_frontLeftPositionSensor(), 1) 
            robot.vaciarCola()
            
            while((not objAlcanzado)and(j<=self.pasos)):
                print("----------------------Paso ",j,"----------------------------------")
                antValPos[0] = actValPosIzq
                antValPos[1] = actValPosDer

                estAct = estSig
                accion = siguienteAccion

                print("Estado Actual: ", estAct,". Acción: ",accion)


                robot.ejecutarComportamiento(accion)

                estSig = robot.estadoActual()
                siguienteAccion = robot.siguienteAccion(estAct)

                print("Estado Siguiente: ", estAct,". Acción: ",siguienteAccion)

                recompensa = self.determinarRecompensa(robot,antValPos)
                
                robot.actualizarPoliticas(estAct,accion,estSig,siguienteAccion,recompensa)

                actValPosDer = round(robot.get_frontRightPositionSensor(), 1)
                actValPosIzq = round(robot.get_frontLeftPositionSensor(), 1)

                
                j += 1
                if(recompensa == self.recompensaMaxima):
                    objAlcanzado = True

            self.puntoInicial(uInicial,rInicial)            




    def ubicacionActual(self):
        self.supervisor.step(self.timestep) 
        return self.translation.getSFVec3f()

    def rotacionActual(self):
        self.supervisor.step(self.timestep) 
        return self.rotation.getSFRotation()

    def puntoInicial(self,posicionInicial, rotacionInicial):
        self.translation.setSFVec3f(posicionInicial)
        self.rotation.setSFRotation(rotacionInicial)
        self.supervisor.simulationResetPhysics()
    
    def get_toleranciaMovimiento(self):
        return self.toleranciaMovimiento

    def set_toleranciaMovimiento(self, value):
        self.toleranciaMovimiento = value
