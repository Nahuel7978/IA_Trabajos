import numpy as np

class Entorno():

    def __init__(self, metrosY, metrosX, pInicial):
        self.mapa = np.zeros(shape=(metrosX,metrosY))
        self.posicionInicial = pInicial
        self.valorPaso = -1
        self.penalizacion = -10
        self.gratificacion = 100
    
    def getTamanoMapa(self):
        return self.mapa.shape
    
    def 