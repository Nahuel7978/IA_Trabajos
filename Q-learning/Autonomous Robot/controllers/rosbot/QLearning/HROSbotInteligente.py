
from QLearning.HROSbot import * 
from QLearning.Entorno import * 
import numpy as np

class HROSbotInteligente(HROSbot):
    def __init__(self, bot, entorno, l_rate, t_descuento, r_exploracion):
        super().__init__(bot)

        self.learning_rate =l_rate
        self.tasa_descuento = t_descuento #si esta cerca de 1 busca las recompensas lejanas
        self.prob_exploracion = r_exploracion
        self.cantidadAcciones = 4

        tam = entorno.getTamanoMapa()
        self.qLearning = np.zeros(shape=(tam[0],tam[1],self.cantidadAcciones))
    
    def siguientePaso(self, posicionActual):
        explorar = np.random.uniform()
        sigPaso = 0

        if(self.prob_exploracion<=explorar):
            sigPaso = np.random.randint(self.cantidadAcciones)
        else:
            sigPaso = np.argmax(self.qLearning[posicionActual])

        return sigPaso

    def actualizarQlearning(self, posicionActual, accionTomada, posicionSiguiente, recompensa):
        max_qsig = np.argmax(self.qLearning[posicionSiguiente])

        qActual = self.qLearning[posicionActual][accionTomada]

        self.qLearning[posicionActual][accionTomada] = qActual + (self.learning_rate*(recompensa+(self.tasa_descuento*max_qsig)-qActual))

    
    