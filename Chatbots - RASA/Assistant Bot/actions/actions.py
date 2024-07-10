# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"



#from pickle import NONE
#from re import M
from asyncio.windows_events import NULL
from atexit import register
from cgitb import text
from email import message
from operator import truth
from tracemalloc import start
from typing import Any, Text, Dict, List
from unittest import result
from urllib import request

#
from rasa_sdk import Action, Tracker
from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from pyswip import Prolog
import os.path
import json

import wikipedia
from googlesearch import search 
#
#
#
class TrabajarArchivo():
    @staticmethod
    def guardar(Guardar):
        with open(".\\actions\\registro","w") as archivo_descarga:
            json.dump(Guardar, archivo_descarga)
        archivo_descarga.close()

    @staticmethod
    def cargarArchivo(): 
        if os.path.isfile(".\\actions\\registro"):
            with open(".\\actions\\registro","r") as archivo_carga:
                ret=json.load(archivo_carga)
                archivo_carga.close()
        else:
            ret={}
        return ret

#
class know_person(Action):
    def name(self)->Text:
        return "person"

    def make_contact(self,message,name,professor,register):
        id = message["metadata"]["message"]["from"]["id"]
        register[id] = {}
        if(name!=None):
            register[id]["name"]= name
        else:
            register[id]["name"]= message["metadata"]["message"]["from"]["first_name"]
    
        register[id]["professor"]= professor
        register[id]["bot"] = message["metadata"]["message"]["from"]["is_bot"]
        register[id]["cut"]=0
        
        TrabajarArchivo.guardar(register)

    def i_am_bot(self,dispatcher)->List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"Soy Nahuel-bot, el Asistente virtual de Nahuel Román, mi creador. Nací 14/09/2022 con el proposito de interactuar con compañeros y profesores de Nahuel. Ayudando con la facultad(info., temas y bibliografia), organizando reuniones, opinando y aconsejando como él lo haria.")
        return []

    def tip(self,dispatcher,id)-> List[Dict[Text, Any]]:
        register = TrabajarArchivo.cargarArchivo()
        if((register!={})&(register.get(str(id),None)!=None)):
            if(register[str(id)]["professor"]):
                dispatcher.utter_message(text=f"que consejo daria... Y creo que un buen consejo que podria darle a un profesor seria que lo más importante debé ser el generar entusiasmo en el alumno, no importa la dificultad, ni la materia; lo importante es que el alumno sienta que está aprendiendo algo que sirve ó le da un feedback positivo alto. Así nunca los vas a perder.")
            else:
                dispatcher.utter_message(text=f"que consejo daria... Y creo que un buen consejo seria que sigas adelante, no importa lo dificil que sea si es el camino que queres para vos, lo importante es seguir. Buscale la vuelta al problema que afrontes y si tenes que sacrificar algo en pos de tu bienestar o lo que anhelas hacelo, pero siempre con convicción.")
        else:
            dispatcher.utter_message(text=f"Perdon, no te tengo agendado, quien sos?")
        return[]
    
    def saludo(self,dispatcher,tracker,last_intent,message,id)-> List[Dict[Text, Any]]:
        register = TrabajarArchivo.cargarArchivo()
        if((register!={})&(register.get(str(id),None)!=None)):
            name = register[str(id)]["name"]
            if(register[str(id)]["professor"]):
                dispatcher.utter_message(text=f"Hola, "+str(name)+", cómo estas? Qué puedo hacer por vos?")
                return[SlotSet(key="name",value=str(name)), SlotSet(key="professor",value=None)]
            else:
                dispatcher.utter_message(text=f"Buenass, "+str(name))
                return[SlotSet(key="name",value=str(name)), SlotSet(key="professor",value=None)]
        else:
            name= next(tracker.get_latest_entity_values("nombre"), None)
            professor= tracker.get_slot("professor")
            if((professor == None)|(last_intent == "saludo")):
                dispatcher.utter_message(text=f"Hola, cómo estas? che, perdon no te tengo agendado, quién sos?")
            else:
                self.make_contact(message,name,professor,register)
                register = TrabajarArchivo.cargarArchivo();
                name = register[str(id)]["name"]
                if(professor):
                    dispatcher.utter_message(text=f"sii, "+str(name)+", qué puedo hacer por vos?")
                    return[SlotSet(key="name",value=str(name)), SlotSet(key="professor",value=professor)]      
                else:
                    dispatcher.utter_message(text=f"Ahh, que onda "+str(name)+"?")
                return[SlotSet(key="name",value=str(name)), SlotSet(key="professor",value=professor)]
        return[]

    def run(self,dispatcher: CollectingDispatcher, tracker:Tracker ,domain: Dict[Text,Any])-> List[Dict[Text, Any]]:
        message = tracker.latest_message
        last_intent = str(tracker.get_intent_of_latest_message())
        id= message["metadata"]["message"]["from"]["id"]
        chat = message["metadata"]["message"]["chat"]["type"]
        entities=" "
        try:
            ent=message["metadata"]["message"]["entities"]
            entities=str(ent[0]["type"])
        except:
            pass

        if((last_intent=="consejo")&(str(chat)!="group")):
            return self.tip(dispatcher,id)
        elif((last_intent=="preguntas_casete")&((str(chat)=="private")|(str(entities)=="mention"))):
            return self.i_am_bot(dispatcher)
        elif((last_intent!="consejo")&(last_intent!="preguntas_casete")):
            return self.saludo(dispatcher,tracker,last_intent,message,id)
        else:
            return[]      

#
class help(Action):
    def name(self):
        return "help_you"
    
    def cutting(self,tracker,dispatcher,last_intent):
        message = tracker.latest_message
        id = message["metadata"]["message"]["from"]["id"]
        register = TrabajarArchivo.cargarArchivo()
        nCut = int(register[str(id)]["cut"])
        if(last_intent=="cortante"):
            nCut+=1
            if(nCut>=3):
                dispatcher.utter_message(text=f"Estas bien "+str(register[str(id)]["name"])+"? Perdon por la pregunta es que te noto un poco cortante. Capaz solo es una sensación y me equivoco.")
                register[str(id)]["cut"] = 0
            else:
                dispatcher.utter_message(text=f"Bueno, que puedo hacer por vos?")
                register[str(id)]["cut"] = nCut
        else:
            dispatcher.utter_message(text=f"Geniall... Hay algo más en lo que pueda ayudar?")
            if(nCut!=0):
                nCut=nCut-1
                register[str(id)]["cut"] = nCut

        TrabajarArchivo.guardar(register)

    def run(self,dispatcher: CollectingDispatcher, tracker:Tracker ,domain: Dict[Text,Any])-> List[Dict[Text, Any]]:
        last_intent = str(tracker.get_intent_of_latest_message())

        if((last_intent=="cortante")|(last_intent=="satisfactorio")):
            self.cutting(tracker,dispatcher,str(last_intent))
        elif(last_intent=="insatisfactorio"):
            dispatcher.utter_message(text=f"que mal, como puedo solucionar esa situción")
        else:
            dispatcher.utter_message(text=f"Hay algo en lo que pueda ayudar?")
        
        return []

#
class materias(Action):
    def name(self)->Text:
        return "subject"
    
    def run(self,dispatcher: CollectingDispatcher, tracker:Tracker, domain: Dict[Text,Any])-> List[Dict[Text, Any]]:
        message = tracker.latest_message
        chat = message["metadata"]["message"]["chat"]["type"]
        entities=" "
        try:
            ent=message["metadata"]["message"]["entities"]
            entities=str(ent[0]["type"])
        except:
            pass
        
        if((str(chat)=="private")|(str(entities)=="mention")):
            prolog=Prolog()
            prolog.consult('/RASA/chat-bot Alumno/actions/reglas_nahuel.pl')
            dispatcher.utter_message(text=f"Estoy cursando:")
            for materia in prolog.query("materia_cursada(X,_,_,_)"):
                dispatcher.utter_message(text=f"- "+str(materia["X"])+"")
        return[]

#
class coordinate(Action):
    def name(self)->Text:
        return "coordinate"
    
    def run(self,dispatcher: CollectingDispatcher, tracker:Tracker, domain: Dict[Text,Any])-> List[Dict[Text, Any]]:
        message = tracker.latest_message
        id= message["metadata"]["message"]["from"]["id"]
        register = TrabajarArchivo.cargarArchivo();
        if((register=={})|(register.get(str(id),None)==None)):
            dispatcher.utter_message(text=f"che, perdon no te tengo agendado, quién sos?")
        else:
            professor = tracker.get_slot("professor")
            if(professor):
                dispatcher.utter_message(text=f"Okey, qué día y a qué hora te convendria?")
            else:
                dispatcher.utter_message(text=f"dale dale, qué día podes?")
                
        return[]
 
class meetings(Action):
    def name(self)->Text:
        return "meet"

    def breakdown_hour(self,time):
        if(str(time).find(':')!=-1):
            (h,m)=str(time).split(':')
            hora=int(h)
            minutos=int(m)
        else:
            hora=int(time)
            minutos=0

        return (hora,minutos)  

    def reuniones_programadas(self,day) -> List[Dict[Text, Any]]:
        register = TrabajarArchivo.cargarArchivo();
        reunion_programadas=[]
        reunion_persona=[];
        for person in register:
            reunion_dia="."
            if(register.get(person).get("meet",None)!=None):
                reunion_dia=str(register.get(person).get("meet").get("day"))

            if(str(reunion_dia)==str(day)):
                hour=register.get(person).get("meet").get("hour")
                hora_inicio,minutos=self.breakdown_hour(hour)

                hora_final = hora_inicio+1

                inicio= str(hora_inicio)+":"+str(minutos)
                fin= str(hora_final)+":"+str(minutos)

                reunion_persona.append(inicio)
                reunion_persona.append(fin)
                reunion_programadas.append(reunion_persona)
                reunion_persona.clear()

        return reunion_programadas

    def offer_schedules(self,dispatcher,Lista_horarios,Lista_reuniones,day,hour)-> List[Dict[Text, Any]]:

        reunion_sugerida=None

        if(hour==None):
            subLista = Lista_horarios[0]
            if((float(subLista[0])>=9))&((float(subLista[0])<13)):
                reunion_sugerida=str(subLista[0]-1)
            else:
                if(float(subLista[1])<=21):
                    reunion_sugerida=str(subLista[1])
        else:   
            hora,minutos=self.breakdown_hour(hour)
            i=0
            h_sug=0
            while((i<len(Lista_horarios))&(reunion_sugerida==None)):
                subLista=Lista_horarios[i]
                hora_inicio_H,minutos_inicio_H=self.breakdown_hour(subLista[0])
                hora_fin_H,minutos_fin_H=self.breakdown_hour(subLista[1])

                if((hora==int(hora_inicio_H))&(int(hora_inicio_H)>=9)):
                            h_sug=int(hora_inicio_H)-1
                            m_sug=int(minutos_inicio_H)
                            reunion_sugerida=str(h_sug)+":"+str(m_sug)
                else:
                    if((hora<int(hora_fin_H))&(int(hora_fin_H)<=21)):
                        h_sug=int(hora_fin_H)
                        m_sug=int(minutos_fin_H)    
                        reunion_sugerida=str(h_sug)+":"+str(m_sug)
                i+=1
            j=0;
            while((j<len(Lista_reuniones))&(reunion_sugerida!=None)):
                subListaReuniones = Lista_reuniones[j]
                hora_inicio_R,minutos_inicio_R=self.breakdown_hour(subListaReuniones[0])
                hora_fin_R,minutos_R=self.breakdown_hour(subListaReuniones[1])
                if(int(h_sug)>=int(hora_inicio_R)&(int(h_sug)<int(hora_fin_R))):
                    reunion_sugerida=None
                j+=1

        if(reunion_sugerida==None):
            dispatcher.utter_message(text=f"Qué otro día te queda comodo? Justo se me complica el "+str(day)+"")
            return[]
        else:
            dispatcher.utter_message(text=f"Te parece a las "+str(reunion_sugerida)+"hs ?")
            return[SlotSet(key="day",value=str(day)),SlotSet(key="hour",value=str(reunion_sugerida))]
    
    def confirm_meet(self,dispatcher,Lista_horarios,Lista_reuniones,day,hour)-> List[Dict[Text, Any]]:
        hora,minutos=self.breakdown_hour(hour)

        i=0
        reunion = True
        while(i<len(Lista_horarios)):
            sub_lista = Lista_horarios[i]
            hora_inicio,minutos_inicio=self.breakdown_hour(sub_lista[0])
            hora_fin,minutos_inicio = self.breakdown_hour(sub_lista[1])
            if((int(hora)>=int(hora_inicio))&(int(hora)<int(hora_fin))):
                reunion=False
            else:
                if((int(hora)==int(hora_inicio)-1)&(int(minutos)>int(minutos_inicio))):
                    reunion=False
            i+=1

        i=0
        while(i<len(Lista_reuniones)):
            sub_lista_r = Lista_reuniones[i]
            hora_inicio,minutos_inicio=self.breakdown_hour(sub_lista_r[0])
            hora_fin,minutos_inicio = self.breakdown_hour(sub_lista_r[1])
            if((int(hora)>=int(hora_inicio))&(int(hora)<=int(hora_fin))):
                reunion=False
            else:
                if((int(hour)>=int(hora_inicio)-1)&(int(minutos)>int(minutos_inicio))):
                    reunion=False
            i+=1
            
        if(reunion):
            dispatcher.utter_message(text=f"Dale dale, entonces ¿el "+str(day)+" a las "+str(hour)+" hs no?.")
            return[SlotSet(key="day",value=str(day)),SlotSet(key="hour",value=str(hour))]
        else:
            dispatcher.utter_message(text=f"uy, se me re complica")
            return self.offer_schedules(dispatcher,Lista_horarios,Lista_reuniones,day,hour)

    def make_meet(self,tracker,day,hour):
        register = TrabajarArchivo.cargarArchivo();
        ms = tracker.latest_message
        id= ms["metadata"]["message"]["from"]["id"]
        register[str(id)]["meet"]={}
        register[str(id)]["meet"]["day"]=day
        register[str(id)]["meet"]["hour"]=hour

        TrabajarArchivo.guardar(register)

    def run(self,dispatcher: CollectingDispatcher, tracker:Tracker, domain: Dict[Text,Any])-> List[Dict[Text, Any]]:
        message = tracker.latest_message
        professor= tracker.get_slot("professor")
        last_intent = str(tracker.get_intent_of_latest_message())
        
            

        if(last_intent=="negacion"):
            dispatcher.utter_message(text=f"Qué otra hora o día te queda comodo?")
            return []
        else:        
            if(last_intent=="horario"):
                day= next(tracker.get_latest_entity_values("dia"), None)
                hour= next(tracker.get_latest_entity_values("hora"), None)

                if(day==None):
                    dispatcher.utter_message(text=f"¿Qué día te parece bien?.")
                    return[]
                else:
                    register = TrabajarArchivo.cargarArchivo();
                    message = tracker.latest_message
                    person=register.get(str(message["metadata"]["message"]["from"]["id"]),None)
                    if(person==None):
                        dispatcher.utter_message(text=f"Perdon, no te tengo agendado, quien sos?")
                    else:
                        meet =register.get(str(message["metadata"]["message"]["from"]["id"])).get("meet",None)
                        meet_day=None

                        if(meet!=None):
                            meet_day=register.get(str(message["metadata"]["message"]["from"]["id"])).get("meet").get("day",None)

                        day= str(day).lower()
                        if((meet_day==None)|(str(meet_day)!=str(day))):
                            prolog = Prolog()
                            prolog.consult('/RASA/chat-bot Alumno/actions/reglas_nahuel.pl')

                            if(professor):
                                consult_horarios = next(prolog.query("horario_ocupado_profesor("+str(day)+", X)"))
                            else:
                                consult_horarios= next(prolog.query("horario_ocupado_alumno("+str(day)+", X)"))
                                
                            horarios=list(consult_horarios["X"])
                            lista_reuniones= self.reuniones_programadas(day) 

                            if(hour ==None):
                                return self.offer_schedules(dispatcher,horarios,lista_reuniones,day,hour)
                            else:
                                return self.confirm_meet(dispatcher,horarios,lista_reuniones,day,hour)
                        else:
                            dispatcher.utter_message(text=f"Ese día tenemos una reunion agendada, te parece coordinar otra para otro día?")
            else:
                day=tracker.get_slot("day")
                hour= tracker.get_slot("hour")
                dispatcher.utter_message(text=f"Genial, ahi lo agendo")
                self.make_meet(tracker,day,hour)
                return[SlotSet(key="day",value=None),SlotSet(key="hour",value=None)]
        
#
class searching(Action):
    def name(self)->Text:
        return "search"

    def busqueda_google(self,dispatcher,busqueda):
        dispatcher.utter_message(text=f"Te dejo unos links de google donde seguro encontras más info: ")
        for resul in search(busqueda, lang='es',num=3, start=0, stop = 3, pause=1):
            dispatcher.utter_message(text=f"- Link: "+str(resul)+"")

    def run(self,dispatcher: CollectingDispatcher, tracker:Tracker, domain: Dict[Text,Any])-> List[Dict[Text, Any]]:
        busqueda = next(tracker.get_latest_entity_values("titulo"), None)
        wikipedia.set_lang('es')
        try:
            parrafo=wikipedia.summary(str(busqueda),sentences=2,auto_suggest=True,redirect=True)
            dispatcher.utter_message(text=f"Fijate esto encontre en wikipedia, capaz te sirve: ")
            dispatcher.utter_message(text=f""+str(parrafo)+"")
            self.busqueda_google(dispatcher,busqueda)
        except wikipedia.DisambiguationError as e:
            self.busqueda_google(dispatcher,busqueda)
        
        return []


##D:\anaconda\envs\installingrasa\Lib\site-packages\rasa\core\channels