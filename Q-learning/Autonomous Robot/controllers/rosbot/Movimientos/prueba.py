import numpy as np
from math import ceil,floor

filas = ceil(40/3)
columnas = ceil(50/3)
        
mapa = np.zeros(shape=(20,21,4))


mapa[0,0,1] = 0.5

for i in range(4):
    mapa[1,0,i] = 0.7

print(mapa[0,0])
print(mapa[1,0])
r= (mapa[1][0]-mapa[0][0])

print("np max: ", np.argmax(mapa[0][0]))

"""
for i in range(20):
    for j in range(21):
        for k in range(4):
            print(mapa[i][j][k])
        print("fin k, en j: ",j)
    print("fin j")
"""

