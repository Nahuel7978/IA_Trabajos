import matplotlib.pyplot as plt
import pandas as pd
#from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier,export_text ,plot_tree;


peliculas_entranamiento = pd.read_csv("G:/Mi unidad/Facultad/3er año/Optativas/Aut. e Inteligencia artificial/Trabajos/Algoritmo Arbol Desicion/Datos/datos_entrenamiento_coleccion.csv", encoding= "ISO-8859-1" ,engine="python")
#peliculas_test = pd.read_csv("G:/Mi unidad/Facultad/3er año/Optativas/Aut. e Inteligencia artificial/Trabajos/Algoritmo Arbol Desicion/Datos/Datos_test.csv", encoding= "ISO-8859-1" ,engine="python", on_bad_lines='skip')

peliculas_entr_int = pd.get_dummies(data=peliculas_entranamiento, drop_first=True)

#print(peliculas_entr_int)
objetivo = peliculas_entr_int.le_gusta
decision = peliculas_entr_int.drop(columns='le_gusta')
#print(decision.values)


arbol_desicion = DecisionTreeClassifier(criterion="entropy", max_depth=8)
arbol_desicion = arbol_desicion.fit(decision.values, objetivo.values)


print(export_text(arbol_desicion,feature_names=decision.columns.tolist()))

#cn = ['no_le_gusta','le_gusta']

#plt.figure(figsize=(15, 10))

#plot_tree(decision_tree=arbol_desicion, feature_names=decision.columns.tolist(), class_names=cn, filled=True, fontsize=5)

#fig.savefig('G:/Mi unidad/Facultad/3er año/Optativas/Aut. e Inteligencia artificial/Trabajos/Algoritmo Arbol Desicion/Datos')
plt.show()

pe = []
pe.append(decision.iloc[4].values)
prediction = arbol_desicion.predict(pe)
print(prediction)