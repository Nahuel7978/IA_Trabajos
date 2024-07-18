# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


from pickle import TRUE
#from pickle import NONE
#from re import M
from typing import Any, Text, Dict, List
#
from swiplserver import PrologServer, PrologThread
#

class Meetings():
    def __init__(self,profesor,day,hour,minutes) -> None:
        self.profesor=profesor
        self.day=day
        self.hour=hour
        self.minutes=minutes

    def run(self):
        
        if(self.day==None):
            print("Que dia te parece")
        else:
            Lista_horarios = [] #PREGUNTAR
            #COMO METO UNA LISTA A LA CONSULTA y que me devuelva la lista de prolog
            with PrologMQI(port=8000) as mqi:
                with mqi.create_thread() as prolog_thread:
                    prolog_thread.query_async("consult('C:\\Users\\Usuario\\OneDrive\\Escritorio\\reglas_nahuel.pl')", find_all=False)
                    if(self.profesor):
                        prolog_thread.query_async(f"horario_ocupado_profesor({self.day},Lista_horarios)", find_all=False)
                        if(self.hour ==None):
                            offer_schedules(Lista_horarios)
                        else:
                            confirm_meet(Lista_horarios,self.hour,self.minutes)
                    else:
                        prolog_thread.query_async(f"horario_ocupado_alumno({self.day},Lista_horarios)", find_all=False)
                        if(self.hour ==None):
                            offer_schedules(Lista_horarios)
                        else:
                            confirm_meet(Lista_horarios,self.hour,self.minutes)


    def confirm_meet(Lista_horarios,hour,minutes)-> List[Dict[Text, Any]]:
        if(minutes==None):
            minutes=0;
        i=0
        reunion = True
        while(i<len(Lista_horarios)&(reunion)):
            j=0
            sub_lista = Lista_horarios[i]
            for hora in sub_lista:
                j+=1
                if((j==1) & (hora>hour) & (minutes<=40)):
                    reunion=True
                else:
                    if((j==2) & (hora<=hour)):
                        reunion=True
                    else:
                        reunion=False
            i+=1            
        if(reunion):
            print("Buenisimo, nos vemos ahí entonces.")
            #Aquí hacer un assert de reunion(llamar otro metodo)
        else:
            print("uy, justo ese horario se me complica")
            offer_schedule(Lista_horarios)

        return[]

    def offer_schedules(Lista_horarios)-> List[Dict[Text, Any]]:
        print("OFFER_SCHEDULES")
        #Ofrecer la hora más cerca de la solicitada
        #Si es la hora es NONE, mostrar la primer desocupada
        #Si no es NONE, ofrecer una hora y CAMBIAR el Slot
        ###Qué pasa con los slots cuando uso el checkpoint o cambio de store??

        return[]

reunion = Meetings(True,'LUNES',18,0)
reunion.run()
